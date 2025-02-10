from typing import Any

import pydantic
from pydantic import ValidationError as PydanticValidationError

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import JSONField
from django.utils.deconstruct import deconstructible
from rest_framework import serializers

Schema = type[pydantic.BaseModel] | type[pydantic.RootModel]


@deconstructible
class SchemaValidator:
    schema: Schema

    def __init__(self, schema: Schema) -> None:
        self.schema = schema

    def __call__(self, value: Any) -> None:
        try:
            self.schema.model_validate(value)
        except PydanticValidationError as e:
            raise DjangoValidationError(message=e)


class PydanticJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        if not any(
            isinstance(validator, SchemaValidator)
            for validator in kwargs.get("validators", [])
        ):
            raise ValueError("At least one SchemaValidator must be provided.")

        kwargs.setdefault("encoder", DjangoJSONEncoder)

        super().__init__(*args, **kwargs)


class PydanticJSONFieldMixin:
    def build_standard_field(self, field_name, model_field):
        # noinspection PyUnresolvedReferences
        standard_field = super().build_standard_field(field_name, model_field)

        if isinstance(model_field, PydanticJSONField):
            schemaValidators = [
                validator
                for validator in model_field.validators
                if isinstance(validator, SchemaValidator)
            ]
            if schemaValidators:
                schema = model_field.validators[0].schema
                standard_field = (
                    type(
                        schema.__name__ + "Serializer",
                        (serializers.JSONField,),
                        {"_spectacular_annotation": {"field": schema}},
                    ),
                ) + standard_field[1:]
        return standard_field
