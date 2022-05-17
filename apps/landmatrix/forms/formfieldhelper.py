from django.contrib.postgres.forms import SimpleArrayField
from django.forms import fields, TypedChoiceField, ModelChoiceField
from django.utils.translation import gettext

from apps.landmatrix.forms.fields import (
    JSONDateAreaChoicesField,
    JSONDateChoiceField,
    JSONActorsField,
    JSONExportsField,
)


class JSONFormOutputMixin:
    def as_json(self):
        ret = {}
        for name, field in self.fields.items():
            assert isinstance(field, fields.Field)
            field_json = {
                "label": field.label,
                "class": field.__class__.__name__,
                "required": field.required,
            }
            if (
                field_json["class"] == "CharField"
                and field.widget.__class__.__name__ == "Textarea"
            ):
                field_json["class"] = "TextField"
            if field.help_text:
                field_json["help_text"] = gettext(field.help_text)
            if hasattr(field, "max_length") and field.max_length:
                field_json["max_length"] = field.max_length

            if isinstance(field, TypedChoiceField):
                field_json["choices"] = {x[0]: x[1] for x in field.choices}
            # if isinstance(field, IntegerField):
            #     breakpoint()
            # "min_value": field.min_value,
            # "max_value": field.max_value,
            # field_json["choices"] = {x[0]: x[1] for x in field.choices}
            if isinstance(field, ModelChoiceField):
                field_json["related_model"] = field.queryset.model.__name__
            if isinstance(field, SimpleArrayField):
                if hasattr(field.base_field, "choices"):
                    field_json["choices"] = {
                        x[0]: x[1] for x in field.base_field.choices
                    }
            if isinstance(
                field,
                (
                    JSONDateAreaChoicesField,
                    JSONDateChoiceField,
                    JSONActorsField,
                    JSONExportsField,
                ),
            ):
                field_json["choices"] = {x[0]: x[1] for x in field.choices}

            # if name == "land_area_comment":
            #     breakpoint()

            if name in list(self.attributes.keys()):
                field_json.update(self.attributes[name])

            ret[name] = field_json

        if hasattr(self, "extra_display_fields"):
            ret.update(self.extra_display_fields)
        return ret
