from django import forms
from django.core.cache import cache

from apps.landmatrix.models import HistoricalInvestor, Investor


def get_display_value(field, values, attributes=None, formset=None):
    output = []
    delimiters = ["|", "#", ","]
    if not values:
        return ""
    if isinstance(field, forms.ModelChoiceField):
        # Use cached unfiltered queryset to retrieve object (because some fields use none() for ajax)
        model_name = field.queryset.model._meta.model_name
        # Always query all objects (for caching)
        queryset = field.queryset.model.objects.all()
        choices = cache.get("%s_choices" % model_name)
        if not choices:
            if field.queryset.model in (HistoricalInvestor, Investor):
                choices = dict(
                    ((str(o.pk), str(o.investor_identifier)) for o in queryset)
                )
            else:
                choices = dict(((str(o.pk), str(o)) for o in queryset))
            cache.set("%s_choices" % model_name, choices)
        output = [value and choices.get(str(value), "") or "" for value in values]
    elif isinstance(field, forms.ChoiceField):
        choices = dict((i[:2] for i in field.choices))
        if "NestedMultipleChoiceField" in str(type(field)):
            for choice in field.choices:
                if len(choice) > 2 and choice[2]:
                    choices.update(dict((i[:2] for i in choice[2])))
        output = [value and choices.get(str(value), "") or "" for value in values]
    elif "AreaField" in str(type(field)):  # pragma: no cover
        pass
    elif isinstance(field, forms.MultiValueField) and attributes:
        delimiter = "|"
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
                            if str(k) == attribute["value"]:
                                attribute["value"] = str(v)
                else:
                    for k, v in choices:
                        if str(k) == attribute["value"]:
                            attribute["value"] = str(v)
        # Collect all attributes for date (for multiple choice fields)
        if multiple[0]:
            for attribute in attributes:
                key = "%s:%s" % (
                    attribute["date"] or "",
                    values_count > 2 and attribute["value2"] or "",
                )
                if key in attributes_by_date:  # pragma: no cover
                    if attribute["value"]:
                        attributes_by_date[key][1] += ", " + attribute["value"]
                else:
                    is_current = attribute["is_current"] and "current" or ""
                    attributes_by_date[key] = [is_current, attribute["value"]]
            if values_count > 2:
                output = [
                    delimiters[1].join([d.split(":")[0], a[0], d.split(":")[1], a[1]])
                    for d, a in attributes_by_date.items()
                ]
            else:  # pragma: no cover
                output = [
                    delimiters[1].join([d or "", a[0], a[1]])
                    for d, a in attributes_by_date.items()
                ]
        else:
            for attribute in attributes:
                is_current = attribute["is_current"] and "current" or ""
                # Value:Value2:Date:Is current
                if values_count > 2:  # pragma: no cover
                    output.append(
                        delimiters[1].join(
                            [
                                attribute["date"] or "",
                                is_current,
                                attribute["value2"],
                                attribute["value"],
                            ]
                        )
                    )
                # Value:Date:Is current
                elif values_count > 1:
                    output.append(
                        delimiters[1].join(
                            [attribute["date"] or "", is_current, attribute["value"]]
                        )
                    )
                # Value:Value2 (e.g. Actors field)
                else:
                    output.append(
                        delimiters[1].join(
                            [attribute["value"], attribute["value2"] or ""]
                        )
                    )
    # elif isinstance(field, forms.FileField):
    #    output = values
    elif isinstance(field, forms.BooleanField):
        output = [value and "Yes" or "No" for value in values]
    # else:
    #    output = [str(value) for value in values]

    # Strip values
    output = [str(i).strip() for i in output]

    if formset:
        return output
    else:
        return delimiters[0].join(output)


def get_spatial_properties():
    keys = []
    from apps.grid.forms.deal_spatial_form import DealSpatialForm

    for key in DealSpatialForm.base_fields.keys():
        if key.startswith("tg_") and not key.endswith("_comment"):
            continue
        keys.append(key)
    return keys


def has_perm_approve_reject(user, object=None):
    """
    Check if user has permission to approve/reject given activity (or investor)
    :param user:
    :param object: activity (or investor)
    :return:
    """
    # Superuser or Admin?
    if user.is_superuser or user.has_perm("landmatrix.change_activity"):
        return True
    # Editor
    elif user.has_perm("landmatrix.review_activity") and object:
        # for editors:
        # only activites that have been added/changed by public users
        # and not been reviewed by another editor yet
        if not object.history_user or not object.history_user.has_perm(
            "landmatrix.review_activity"
        ):
            for changeset in object.changesets.exclude(fk_user=user):
                if changeset.fk_user and changeset.fk_user.has_perm(
                    "landmatrix.review_activity"
                ):
                    return False
        return True
    # FIXME: Maybe check for country/region here in the future (FilteredQuerySetMixin.get_filtered_activity_queryset)
    return False
