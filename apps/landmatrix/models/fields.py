from typing import Iterable

from django import forms
from django.contrib.postgres.fields import ArrayField as _ArrayField
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from fastjsonschema import JsonSchemaException

from apps.landmatrix.models.schemas import (
    contracts_schema,
    locations_schema,
    datasources_schema,
)


class ArrayField(_ArrayField):
    def value_to_string(self, obj):
        return self.value_from_object(obj)


class JSONSchemaField(JSONField):
    schema_defition = None

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        self.validate_schema(value)
        return value

    @classmethod
    def validate_schema(cls, value):
        if value:  # do schema validation here
            try:
                cls.schema_defition(value)
            except JsonSchemaException as e:
                raise ValidationError(e, code="invalid")

    def formfield(self, **kwargs):
        current_class = self.__class__

        class JSONSchemaFormField(forms.JSONField):
            def to_python(self, value):
                value = super().to_python(value)
                current_class.validate_schema(value)
                return value

        return super().formfield(**{"form_class": JSONSchemaFormField, **kwargs})

    # def from_db_value(self, value, expression, connection):
    #     if value is None:
    #         return value
    #     # we could do conversion to datefield here
    #     return value


class LocationsField(JSONSchemaField):
    schema_defition = locations_schema


class ContractsField(JSONSchemaField):
    schema_defition = contracts_schema


class DatasourcesField(JSONSchemaField):
    schema_defition = datasources_schema


# class JSONDateAreaChoicesField(JSONField):
#     def _check_choices(self):
#         return []
#
#     def __init__(self, *args, **kwargs):
#         if kwargs.get("choices"):
#             self.choices = [x[0] for x in kwargs.get("choices")]
#         super().__init__(*args, **kwargs)
#
#     def pre_save(self, model_instance, add):
#         value = super().pre_save(model_instance, add)
#         self.validate_schema(value, self.choices)
#         return value
#
#     @staticmethod
#     def validate_schema(value, choices):
#         date_area_choices_def = {
#             "$schema": "http://json-schema.org/draft-07/schema#",
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "additionalProperties": False,
#                 "properties": {
#                     "current": {"type": ["boolean", "null"]},
#                     "name": {"type": "string"},
#                     "area": {"type": ["string", "null"]},
#                     "choices": {
#                         "type": "array",
#                         "items": {"type": "string", "enum": choices},
#                     },
#                 },
#             },
#         }
#         schema = compile(date_area_choices_def)
#         try:
#             schema(value)
#         except JsonSchemaException as e:
#             raise ValidationError(e, code="invalid")
#
#     def formfield(self, **kwargs):
#         validate_schema = self.validate_schema
#         choices = [x[0] for x in self.choices]
#         self.choices = None
#
#         class JSONDateAreaChoicesFormField(forms.JSONField):
#             def to_python(self, value):
#                 value = super().to_python(value)
#                 validate_schema(value, choices)
#                 return value
#
#         return super().formfield(
#             **{"form_class": JSONDateAreaChoicesFormField, **kwargs}
#         )
