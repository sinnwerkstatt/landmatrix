import re
from collections import OrderedDict

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.datastructures import MultiValueDict
from django.utils.translation import gettext_lazy as _

from apps.grid.fields import (
    ActorsField,
    AreaField,
    MultiCharField,
    NestedMultipleChoiceField,
    YearBasedField,
)
from apps.grid.utils import get_display_value


class FieldsDisplayFormMixin(object):
    def get_fields_display(self, user=None):
        """Return fields for detail view"""
        output = []
        tg_title = ""
        tg_items = []
        for i, (field_name, field) in enumerate(self.base_fields.items()):

            if field_name.startswith("tg_") and not field_name.endswith("_comment"):
                #    value = self.initial.get(self.prefix and "%s-%s"%(self.prefix, field_name) or field_name, [])
                #    if field_name == 'tg_nature_comment':
                #        raise IOError(value)
                #    if value:
                #        tg_items.append(field.label, value))
                #    continue
                if len(tg_items) > 0:
                    output.append({"name": "tg", "label": "", "value": tg_title})
                    output.extend(tg_items)
                tg_title = field.initial
                tg_items = []
                continue
            if isinstance(field, NestedMultipleChoiceField):
                value = self.get_display_value_nested_multiple_choice_field(
                    field, field_name
                )
            elif isinstance(
                field, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)
            ):
                value = self.get_display_value_multiple_choice_field(field, field_name)
            elif isinstance(field, forms.ModelChoiceField):
                value = self.get_display_value_model_choice_field(field, field_name)
            elif isinstance(field, forms.ChoiceField):
                value = self.get_display_value_choice_field(field, field_name)
            elif isinstance(field, AreaField):
                value = self.get_display_value_area_field(field, field_name)
            elif isinstance(field, forms.MultiValueField):
                value = self.get_display_value_multi_value_field(field, field_name)
            elif isinstance(field, forms.FileField):
                value = self.get_display_value_file_field(field, field_name)
            elif isinstance(field, forms.BooleanField):
                value = self.get_display_value_boolean_field(field, field_name)
            else:
                value = self.initial.get(field_name, "")

            if value:
                tg_items.append(
                    {
                        "name": field_name,
                        "label": field.label,
                        "value": value,
                        # 'value': '%s %s' % (value, field.help_text),
                    }
                )

        if len(tg_items) > 0:
            output.append({"name": "tg", "label": "", "value": tg_title})
            output.extend(tg_items)
        return output

    def get_display_value_boolean_field(self, field, field_name):
        data = self.initial.get(
            field_name, ""
        )  # self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, '')
        if data == "True":
            return _("Yes")
        elif data == "False":
            return _("No")
        return ""

    def get_display_value_file_field(self, field, field_name):
        value = self.initial.get(field_name, "")
        return value

    def get_display_value_multi_value_field(self, field, field_name):
        # todo - fails with historical deals?
        data = self.initial.get(
            field_name, ""
        )  # self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, '')
        values = []
        if data:
            for value in data.split("#"):
                date_values = value.split(":")
                current = date_values.pop() if date_values else None
                date = date_values.pop() if date_values else None
                if date_values:
                    # Replace value with label for choice fields
                    if isinstance(field.fields[0], forms.ChoiceField):
                        selected = date_values[0].split(",")
                        # Grouped choice field?
                        if isinstance(
                            list(field.fields[0].choices)[0][1], (list, tuple)
                        ):
                            date_values[0] = []
                            for group, items in field.fields[0].choices:
                                date_value = ", ".join(
                                    [str(l) for v, l in items if str(v) in selected]
                                )
                                if date_value:
                                    date_values[0].append(date_value)
                            date_values[0] = ", ".join(date_values[0])
                        else:
                            date_values[0] = ", ".join(
                                [
                                    str(l)
                                    for v, l in field.fields[0].choices
                                    if str(v) in selected
                                ]
                            )
                    value = ""
                    if date or current:
                        value += "[%s] " % ", ".join(
                            filter(None, [date, (current and "current" or "")])
                        )
                    value += date_values[0]
                    if len(date_values) > 1:
                        value2 = ", ".join(filter(None, date_values[1:]))
                        if value2:
                            value += _(" (%s %s)") % (
                                value2,
                                hasattr(field, "placeholder")
                                and field.placeholder
                                or "ha",
                            )
                else:
                    value = ""
                if value:
                    values.append(value)
        return "<br>".join(values)

    def get_display_value_choice_field(self, field, field_name):
        data = self.initial.get(field_name)
        if not data:
            data = []
        value = "<br>".join([str(l) for v, l in field.choices if v and str(v) in data])
        return value

    #    def get_list_from_initial(self, field_name):
    #        if isinstance(self.initial, MultiValueDict):
    #            return self.initial.getlist(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
    #        data = self.initial.get(field_name, [])#self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
    #        if data: data = [data]
    #        return data

    def get_display_value_area_field(self, field, field_name):
        data = self.initial.get(
            field_name, []
        )  # self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        if data:
            # Return serialized value for map
            widget = field.widget.widgets[0]
            context = widget.get_context("contract_area", data)
            return {"srid": widget.map_srid, "serialized": context["serialized"]}
        else:
            return {}

    def get_display_value_multiple_choice_field(self, field, field_name):
        data = self.initial.get(
            field_name, []
        )  # self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        value = "<br>".join([str(l) for v, l in field.choices if str(v) in data])
        return value

    def get_display_value_nested_multiple_choice_field(self, field, field_name):
        data = self.initial.get(
            field_name, []
        )  # self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        values = []
        for v, l, c in field.choices:
            value = ""
            if str(v) in data:
                value = str(l)
            if c:
                choices = ", ".join([str(l) for v, l in c if str(v) in data])
                value = (value and "%s (%s)" % (value, choices)) or choices
            if value:
                values.append(value)
        value = "<br>".join(values)
        return value

    def get_display_value_model_choice_field(self, field, field_name):
        value = self.initial.get(
            field_name, []
        )  # self.prefix and "%s-%s" % (self.prefix, field_name) or field_name, [])
        if value:
            try:
                # Use base queryset to handle none() querysets (used with ajax based widgets)
                object = field.queryset.model.objects.get(pk=value)
            except (ValueError, AttributeError, ObjectDoesNotExist):
                return ""

            # Return links for some specific fields, maybe better move to the respective form
            if field_name in ("operational_stakeholder", "fk_investor"):
                url = reverse(
                    "investor_detail",
                    kwargs={
                        "investor_id": object.investor_identifier,
                        #'history_id': object.id,
                    },
                )
                value = '<a href="%s">%s</a>' % (url, str(object))
            else:
                value = str(object)
        else:
            value = ""

        return value

    @classmethod
    def get_display_properties(cls, doc, formset=None):
        """Get field display values for ES"""
        output = {}
        for name, field in cls.base_fields.items():
            # Title field?
            if name.startswith("tg_") and not name.endswith("_comment"):
                continue
            key = "%s_display" % name

            values = doc.get(name)
            if not values:
                output[key] = []
                continue
            if not isinstance(values, (list, tuple)):
                values = [values]
            attr_key = "%s_attr" % name
            attributes = attr_key in doc and doc.get(attr_key) or None

            value = get_display_value(field, values, attributes, formset=formset)
            if value:
                output[key] = value
        return output


class BaseForm(FieldsDisplayFormMixin, forms.Form):

    error_css_class = "error"

    def get_attributes(self, request=None):
        """
        Get posted form data, for saving to the database.
        For activity or stakeholder, using attribute group only - if given
        (for formsets)
        """
        attributes = OrderedDict()
        for i, (n, f) in enumerate(self.fields.items()):
            name = str(n)
            # New tag group?
            if n.startswith("tg_") and not n.endswith("_comment"):
                continue
            if isinstance(
                f, (forms.ModelMultipleChoiceField, forms.MultipleChoiceField)
            ):
                # Create tags for each value
                value = self.data.getlist(
                    self.prefix and "%s-%s" % (self.prefix, n) or n, []
                )
                values = []
                for v in list(value):
                    if v:
                        try:
                            # Save display value
                            # FIXME: We should save the value instead, now that we have _display fields
                            value = str(dict([i[:2] for i in f.choices])[v])
                        except (ValueError, TypeError, KeyError):
                            value = None
                        if isinstance(f, NestedMultipleChoiceField) and not value:
                            for choice in f.choices:
                                try:
                                    value = str(dict([i[:2] for i in choice[2]])[v])
                                    if value:
                                        break
                                except (ValueError, TypeError, KeyError):
                                    value = None
                        if not value:
                            value = v
                        if value:
                            values.append({"value": value})
                if values:
                    attributes[name] = values
            elif isinstance(f, forms.ModelChoiceField):
                value = self.data.get(self.prefix and "%s-%s" % (self.prefix, n) or n)
                if value:
                    # Save pk of object
                    attributes[name] = {"value": value}
            elif isinstance(f, forms.ChoiceField):
                value = self.data.get(self.prefix and "%s-%s" % (self.prefix, n) or n)
                if value:
                    # Save display value
                    # FIXME: We should save the value instead, now that we have _display fields
                    value = str(dict(f.choices).get(value))
                    if value:
                        attributes[name] = {"value": value}
            # Year based data (or Actors field)?
            elif isinstance(f, (YearBasedField, ActorsField)):
                # Grab last item and enumerate, since there can be gaps
                # because of checkboxes not submitting data
                prefix = self.prefix and "%s-%s" % (self.prefix, n) or "%s" % n
                keys = [
                    int(k.replace(name + "_", ""))
                    for k in self.data.keys()
                    if re.match("%s_\d" % prefix, k)
                ]
                count = len(keys) > 0 and max(keys) + 1 or 0
                widget_count = len(f.widget.get_widgets())
                if count % widget_count > 0:
                    count += 1
                values = []
                for i in range(count):
                    key = "%s_%i" % (prefix, i)
                    if i % widget_count == 0:
                        widget_values = self.data.getlist(key)
                        value2 = None
                        year = None
                        is_current = False
                        # Value / Value2 / Date / is current
                        if widget_count > 3:
                            value2 = self.data.get("%s_%i" % (prefix, i + 1))
                            year = self.data.get("%s_%i" % (prefix, i + 2))
                            is_current = "%s_%i" % (prefix, i + 3) in self.data
                        # Value / Date / is current
                        elif widget_count > 2:
                            year = self.data.get("%s_%i" % (prefix, i + 1))
                            is_current = "%s_%i" % (prefix, i + 2) in self.data
                        # Value / Value2 (e.g. Actors field)
                        elif widget_count == 2:
                            value2 = self.data.get("%s_%i" % (prefix, i + 1))
                        for value in widget_values:
                            if value or value2 or year:
                                values.append(
                                    {
                                        "value": value,
                                        "value2": value2,
                                        "date": year,
                                        "is_current": is_current,
                                    }
                                )
                if values:
                    attributes[name] = values
            elif isinstance(f, forms.FileField):
                value = self.get_display_value_file_field(f, n)
                if value:
                    attributes[name] = {"value": value}
            elif isinstance(f, forms.DecimalField):
                value = (
                    self.is_valid()
                    and self.cleaned_data.get(n)
                    or self.data.get(self.prefix and "%s-%s" % (self.prefix, n) or n)
                )
                if value:
                    attributes[name] = {"value": str(value)}
            elif isinstance(f, forms.FloatField):
                value = (
                    self.is_valid()
                    and self.cleaned_data.get(n)
                    or self.data.get(self.prefix and "%s-%s" % (self.prefix, n) or n)
                )
                if value:
                    # Save integer if whole number
                    if str(value).isdigit():
                        value = int(value)
                    attributes[name] = {"value": str(value)}
            else:
                value = (
                    self.is_valid()
                    and self.cleaned_data.get(n)
                    or self.data.get(self.prefix and "%s-%s" % (self.prefix, n) or n)
                )
                if value:
                    attributes[name] = {"value": value}
        return attributes

    @classmethod
    def get_data(cls, activity, group=None, prefix=""):
        """
        Load previously saved attributes from the database.
        Returns:
        {
            'Name of attribute 1': {
                value: 'Value for attribute',
                value2: 'Optional second value for attribute, e.g. ha for crops',
                date: 'Date of value for year based fields',
            },
            'Name of attribute 2': {
                ...
            }
        }
        """
        data = MultiValueDict()

        # Create attributes dict
        queryset = activity.attributes.order_by("id")
        if group:
            queryset = queryset.filter(fk_group__name=group)
        attributes = OrderedDict()
        for aa in queryset.all():
            if aa.name in attributes:
                attributes[aa.name].append(aa)
            else:
                attributes[aa.name] = [aa]

        for (field_name, field) in cls().base_fields.items():
            # Group title?
            name = prefix and "%s-%s" % (prefix, field_name) or field_name
            if field_name.startswith("tg_") and not field_name.endswith("comment"):
                continue
            # tags, group = cls.get_tags(field_name, activity, group)
            attribute = attributes.get(field_name, [])

            if not attribute:
                continue

            value = attribute[0].value
            # Multiple choice?
            if isinstance(
                field, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField)
            ):
                value = cls.get_multiple_choice_data(field, field_name, attribute)
            # Year based data (or Actors field/MultiCharField)?
            # TODO: check if the other two should be included
            elif isinstance(field, (YearBasedField, MultiCharField, ActorsField)):
                value = cls.get_year_based_data(field, field_name, attribute)
            # Choice field?
            elif isinstance(field, forms.ChoiceField):
                for k, v in field.choices:
                    if v == value:
                        value = str(k)
                        break

            if value:
                data[name] = value
        return data

    @classmethod
    def get_multiple_choice_data(cls, field, field_name, attributes):
        values = []
        for attribute in attributes:
            value = cls.get_multiple_choice_value(field, attribute.value)
            if value:
                values.append(value)
        return values

    @classmethod
    def get_multiple_choice_value(cls, field, tag_value):
        value = cls.get_choice_value(field, tag_value)
        if isinstance(field, NestedMultipleChoiceField) and not value:
            value = cls.get_nested_choice_value(field, tag_value)
        return value

    @classmethod
    def get_nested_choice_value(cls, field, tag_value):
        for choice in field.choices:
            for k, v in [i[:2] for i in choice[2] or []]:
                if k == tag_value or (tag_value.isdigit() and k == int(tag_value)):
                    return str(k)
                # FIXME: Save raw values to the database and remove this after
                if v == tag_value or (tag_value.isdigit() and v == int(tag_value)):
                    return str(k)
        return None

    @classmethod
    def get_choice_value(cls, field, tag_value):
        for k, v in [i[:2] for i in field.choices]:
            if k == tag_value or (tag_value.isdigit() and k == int(tag_value)):
                return str(k)
            # FIXME: Save raw values to the database and remove this after
            if v == tag_value or (tag_value.isdigit() and v == int(tag_value)):
                return str(k)
        return None

    @classmethod
    def get_year_based_data(cls, field, field_name, attributes):
        # Group all attributes by date
        attributes_by_date = OrderedDict()
        # Some year based fields take 2 values, e.g. crops and area
        widgets = field.widget.get_widgets()
        multiple = field.widget.get_multiple()
        values_count = len(widgets) - 1
        values = []

        # Collect all attributes for date (for multiple choice fields)
        if multiple[0]:
            for attribute in attributes:
                key = "%s:%s" % (
                    attribute.date or "",
                    values_count > 2 and attribute.value2 or "",
                )
                if key in attributes_by_date:
                    if attribute.value:
                        attributes_by_date[key][1] += "," + attribute.value
                else:
                    is_current = attribute.is_current and "1" or ""
                    attributes_by_date[key] = [is_current, attribute.value]
            if values_count > 2:
                values = [
                    ":".join([a[1], d.split(":")[1], d.split(":")[0], a[0]])
                    for d, a in attributes_by_date.items()
                ]
            else:
                values = [
                    ":".join([a[1], d or "", a[0]])
                    for d, a in attributes_by_date.items()
                ]  # pragma: no cover
        else:
            for attribute in attributes:
                is_current = attribute.is_current and "1" or ""
                # Value:Value2:Date:Is current
                if values_count > 2:  # pragma: no cover
                    values.append(
                        ":".join(
                            [
                                attribute.value,
                                attribute.value2,
                                attribute.date or "",
                                is_current,
                            ]
                        )
                    )
                # Value:Date:Is current
                elif values_count > 1:
                    values.append(
                        ":".join([attribute.value, attribute.date or "", is_current])
                    )
                # Value:Value2 (e.g. Actors field)
                else:
                    values.append(":".join([attribute.value, attribute.value2 or ""]))
        return "#".join(values)

    @property
    def meta(self):
        # Required for template access to Meta class
        return hasattr(self, "Meta") and self.Meta or None

    class Meta:
        exclude = ()
        fields = ()
        readonly_fields = ()
        name = ""

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        if hasattr(self.Meta, "exclude"):
            for field in self.Meta.exclude:
                del self.fields[field]
        if hasattr(self.Meta, "fields") and self.Meta.fields:
            fields = OrderedDict()
            for field in self.Meta.fields:
                fields[field] = self.fields[field]
            self.fields = fields
        if hasattr(self.Meta, "readonly_fields") and self.Meta.readonly_fields:
            for n in self.Meta.readonly_fields:
                f = self.fields[n]
                if isinstance(f.widget, forms.Select):
                    self.fields[n].widget.attrs["disabled"] = "disabled"
                else:
                    self.fields[n].widget.attrs["readonly"] = True
