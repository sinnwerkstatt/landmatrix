import json

from django import forms
from django.contrib.postgres.fields import ArrayField as _ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import JSONField, CharField, DecimalField
from fastjsonschema import JsonSchemaException, compile

from .choices import (
    ACTOR_ITEMS,
    ELECTRICITY_GENERATION_ITEMS,
    CARBON_SEQUESTRATION_ITEMS,
    CARBON_SEQUESTRATION_CERT_ITEMS,
)

loose_date_re_val = RegexValidator(
    regex=r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
    message="Use yyyy or yyyy-mm or yyyy-mm-dd",
    code="invalid_date",
)


class LooseDateField(CharField):
    default_validators = [loose_date_re_val]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        super().__init__(*args, **kwargs)


class NanoIDField(CharField):
    pass


class DecimalIntField(DecimalField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return float(value)


class ArrayField(_ArrayField):
    def value_to_string(self, obj):
        return self.value_from_object(obj)


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 4.2's postgres ArrayField
    and a TypeMultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(
            models.CharField(max_length=..., choices=(...,)), blank=[...], default=[...]
        )
    """

    class _TypedMultipleChoiceField(forms.TypedMultipleChoiceField):
        def __init__(self, *args, **kwargs):
            kwargs.pop("base_field", None)
            kwargs.pop("max_length", None)
            super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self._TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        # pylint:disable=bad-super-call
        return super().formfield(**defaults)


class JSONSchemaField(JSONField):
    schema_definition = None

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        self.validate_schema(value)
        return value

    def validate_schema(self, value):
        if not value:
            return
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as e:
                raise ValidationError(f"invalid JSON: {e}")

        try:
            self.schema_definition(value)
        except JsonSchemaException as e:
            raise ValidationError(
                message=f"{self.__class__.__name__} '{self.name}': {e}\n{value}",
                code="invalid",
            )

    def formfield(self, **kwargs):
        current_self = self

        class JSONSchemaFormField(forms.JSONField):
            def to_python(self, value):
                current_self.validate_schema(value)
                value = super().to_python(value)
                return value

        return super().formfield(**{"form_class": JSONSchemaFormField, **kwargs})

    # def from_db_value(self, value, expression, connection):
    #     if value is None:
    #         return value
    #     # we could do conversion to datefield here
    #     return value


class JSONCurrentDateAreaField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 3,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number"]},
                    },
                },
            }
        )


class JSONCurrentDateAreaChoicesField(JSONSchemaField):
    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 4,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number", "null"]},
                        "choices": {
                            "type": "array",
                            "items": {"type": "string", "enum": choices or []},
                        },
                    },
                },
            }
        )


class JSONCurrentDateChoiceField(JSONSchemaField):
    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 3,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "choice": {"enum": choices or []},
                    },
                },
            }
        )


class JSONLeaseField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 5,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number", "null"]},
                        "farmers": {"type": ["number", "null"]},
                        "households": {"type": ["number", "null"]},
                    },
                },
            }
        )


class JSONJobsField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 5,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "jobs": {"type": ["number", "null"]},
                        "employees": {"type": ["number", "null"]},
                        "workers": {"type": ["number", "null"]},
                    },
                },
            }
        )


class JSONActorsField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "name": {"type": "string"},
                        "role": {
                            "type": "string",
                            "enum": [x["value"] for x in ACTOR_ITEMS],
                        },
                    },
                },
            }
        )


class JSONExportsField(JSONSchemaField):
    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 6,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "choices": {
                            "type": "array",
                            "items": {"type": "string", "enum": choices or []},
                        },
                        "area": {"type": ["number", "null"]},
                        "yield": {"type": ["number", "null"]},
                        "export": {"type": ["number", "null"]},
                    },
                },
            }
        )


class JSONElectricityGenerationField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [x["value"] for x in ELECTRICITY_GENERATION_ITEMS]
        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 8,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number", "null"]},
                        "choices": {
                            "type": "array",
                            "items": {"type": "string", "enum": choices},
                        },
                        "export": {"type": ["number", "null"]},
                        "windfarm_count": {"type": ["number", "null"]},
                        "current_capacity": {"type": ["number", "null"]},
                        "intended_capacity": {"type": ["number", "null"]},
                    },
                },
            }
        )


class JSONCarbonSequestrationField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [x["value"] for x in CARBON_SEQUESTRATION_ITEMS]
        choices2 = [x["value"] for x in CARBON_SEQUESTRATION_CERT_ITEMS]
        self.schema_definition = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "minProperties": 9,
                    "properties": {
                        "current": {"type": "boolean"},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number", "null"]},
                        "choices": {
                            "type": "array",
                            "items": {"type": "string", "enum": choices},
                        },
                        "projected_lifetime_sequestration": {
                            "type": ["number", "null"]
                        },
                        "projected_annual_sequestration": {"type": ["number", "null"]},
                        "certification_standard": {"type": ["boolean", "null"]},
                        "certification_standard_name": {"enum": choices2},
                        "certification_standard_comment": {"type": "string"},
                    },
                },
            }
        )
