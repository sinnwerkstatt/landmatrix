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


class LocationsField(JSONField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value:  # do schema validation here
            try:
                locations_schema(value)
            except JsonSchemaException as e:
                print(value)
                raise ValidationError(e, code="invalid")
        return value

    # def __init__(self, verbose_name=None, name=None, **kwargs):
    #     # kwargs["encoder"] = DjangoJSONEncoder
    #     super().__init__(verbose_name=verbose_name, name=name, **kwargs)

    # def formfield(self, **kwargs):
    #     return super().formfield(**{
    #         'form_class': forms.JSONField,
    #         **kwargs,
    #     })

    # def from_db_value(self, value, expression, connection):
    #     if value is None:
    #         return value
    #     # we could do conversion to datefield here
    #     return value


class ContractsField(JSONField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value:  # do schema validation here
            try:
                contracts_schema(value)
            except JsonSchemaException as e:
                print(value)
                raise ValidationError(e, code="invalid")
        return value


class DatasourcesField(JSONField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value:  # do schema validation here
            try:
                datasources_schema(value)
            except JsonSchemaException as e:
                print(value)
                raise ValidationError(e, code="invalid")
        return value
