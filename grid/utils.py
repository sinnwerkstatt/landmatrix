from django.core.cache import cache
from django import forms

from landmatrix.models import Investor

def get_export_value(field, values, attributes=None, formset=None):
    output = []
    delimiters = ['|', '#', ',']
    if not values:
        return ''
    if isinstance(field, forms.ModelChoiceField):
        # Use cached unfiltered queryset to retrieve object (because some fields use none() for ajax)
        model_name = field.queryset.model._meta.model_name
        choices = cache.get('%s_choices' % model_name)
        if not choices:
            # FIXME: Performing the queryset here for some reason is incredibly slow
            if field.queryset.model == Investor:
                choices = dict(((str(o.pk), str(o.investor_identifier)) for o in field.queryset))
            else:
                choices = dict(((str(o.pk), str(o)) for o in field.queryset))
            cache.set('%s_choices' % model_name, choices)
        output = [value and choices.get(str(value), '') or '' for value in values]
    elif isinstance(field, forms.ChoiceField):
        for k, v in [i[:2] for i in field.choices]:
            if str(k) in values:
                output.append(str(v))
        if 'NestedMultipleChoiceField' in str(type(field)):
            for choice in field.choices:
                for k, v in [i[:2] for i in choice[2] or []]:
                    if str(k) in values:
                        output.append(str(v))
    elif 'AreaField' in str(type(field)):
        pass
    elif isinstance(field, forms.MultiValueField) and attributes:
        delimiter = '|'
        # Group all attributes by date
        attributes_by_date = dict()
        # Some year based fields take 2 values, e.g. crops and area
        widgets = field.widget.get_widgets()
        multiple = field.widget.get_multiple()
        values_count = len(widgets) - 1
        # Replace value with label for choice fields
        if isinstance(field.fields[0], forms.ChoiceField):
            choices = list(field.fields[0].choices)
            for attribute in attributes:
                # Grouped choice field?
                if isinstance(choices[0][1], (list, tuple)):
                    for group, items in choices:
                        for k, v in items:
                            if str(k) == attribute['value']:
                                attribute['value'] = str(v)
                else:
                    for k, v in choices:
                        if str(k) == attribute['value']:
                            attribute['value'] = str(v)
        # Collect all attributes for date (for multiple choice fields)
        if multiple[0]:
            for attribute in attributes:
                key = '%s:%s' % (attribute['date'] or '', values_count > 2 and attribute['value2'] or '')
                if key in attributes_by_date:
                    if attribute['value']:
                        attributes_by_date[key][1] += ', ' + attribute['value']
                else:
                    is_current = attribute['is_current'] and 'current' or ''
                    attributes_by_date[key] = [is_current, attribute['value']]
            if values_count > 2:
                output = [delimiters[1].join([
                    d.split(':')[0],
                    a[0],
                    d.split(':')[1],
                    a[1],
                ]) for d, a in attributes_by_date.items()]
            else:
                output = [delimiters[1].join([
                    d or '',
                    a[0],
                    a[1],
                ]) for d, a in attributes_by_date.items()]
        else:
            for attribute in attributes:
                is_current = attribute['is_current'] and 'current' or ''
                # Value:Value2:Date:Is current
                if values_count > 2:
                    output.append(delimiters[1].join([
                        attribute['date'] or '',
                        is_current,
                        attribute['value2'],
                        attribute['value'],
                    ]))
                # Value:Date:Is current
                elif values_count > 1:
                    output.append(delimiters[1].join([
                        attribute['date'] or '',
                        is_current,
                        attribute['value'],
                    ]))
                # Value:Value2 (e.g. Actors field)
                else:
                    output.append(delimiters[1].join([
                        attribute['value'],
                        attribute['value2'] or ''
                    ]))
    elif isinstance(field, forms.FileField):
        output = values
    elif isinstance(field, forms.BooleanField):
        output = [value and 'Yes' or 'No' for value in values]
    else:
        output = [str(value) for value in values]

    # Strip values
    output = [str(i).strip() for i in output]

    if formset:
        return output
    else:
        return delimiters[0].join(output)


def get_spatial_properties():
    keys = []
    from grid.forms.deal_spatial_form import DealSpatialForm
    for key in DealSpatialForm.base_fields.keys():
        if key.startswith('tg_') and not key.endswith('_comment'):
            continue
        keys.append(key)
    return keys