from typing import Any

import pydantic
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from pydantic import ValidationError as PydanticValidationError
from rest_framework import serializers


class PydanticJSONField(JSONField):
    description = _("A JSON object with Pydantic schema")

    def __init__(
        self,
        *args,
        schema: type[pydantic.BaseModel] | type[pydantic.RootModel] | None = None,
        # config: pydantic.ConfigDict | None = None,
        **kwargs,
    ):
        self.schema = schema
        # self.config = config

        kwargs.setdefault("encoder", DjangoJSONEncoder)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.update(schema=self.schema)
        return name, path, args, kwargs

    def validate(self, value: Any, model_instance) -> None:
        try:
            self.schema.model_validate(value)
        except PydanticValidationError as e:
            raise DjangoValidationError(message=e)
        return super().validate(value, model_instance)


class PydanticJSONFieldMixin:
    def build_standard_field(self, field_name, model_field):
        # noinspection PyUnresolvedReferences
        standard_field = super().build_standard_field(field_name, model_field)
        if isinstance(model_field, PydanticJSONField):
            standard_field = (
                type(
                    model_field.schema.__name__ + "Serializer",
                    (serializers.JSONField,),
                    {"_spectacular_annotation": {"field": model_field.schema}},
                ),
            ) + standard_field[1:]
        return standard_field
