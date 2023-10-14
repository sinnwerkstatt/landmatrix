from fastjsonschema import JsonSchemaException, compile

from django.core.exceptions import ValidationError
from django.forms import JSONField

from ..models.choices import ACTOR_MAP


class JSONDateAreaChoicesField(JSONField):
    def __init__(self, encoder=None, decoder=None, **kwargs):
        self.choices = kwargs.pop("choices")
        self.choices_keys = []
        for k, v in self.choices:
            if isinstance(v, list | tuple):
                for i, j in v:
                    self.choices_keys += [i]
            else:
                self.choices_keys += [k]
        super().__init__(encoder, decoder, **kwargs)

    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "current": {"type": ["boolean", "null"]},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number", "null"]},
                        "choices": {
                            "type": "array",
                            "items": {"type": "string", "enum": self.choices_keys},
                        },
                    },
                },
            }
        )
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value


class JSONDateAreaField(JSONField):
    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "current": {"type": ["boolean", "null"]},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "area": {"type": ["number", "null"]},
                    },
                },
            }
        )
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value


class JSONDateChoiceField(JSONField):
    def __init__(self, encoder=None, decoder=None, **kwargs):
        self.choices = kwargs.pop("choices")
        self.choices_keys = [None]
        for k, v in self.choices:
            if isinstance(v, list | tuple):
                for i, j in v:
                    self.choices_keys += [i]
            else:
                self.choices_keys += [k]
        super().__init__(encoder, decoder, **kwargs)

    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "current": {"type": ["boolean", "null"]},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "choice": {"enum": self.choices_keys},
                    },
                },
            }
        )
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value


class JSONActorsField(JSONField):
    choices = ACTOR_MAP

    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "name": {"type": "string"},
                        "role": {
                            "type": "string",
                            "enum": [x[0] for x in self.choices],
                        },
                    },
                },
            }
        )
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value


class JSONExportsField(JSONField):
    def __init__(self, encoder=None, decoder=None, **kwargs):
        self.choices = kwargs.pop("choices")
        self.choices_keys = []
        for k, v in self.choices:
            if isinstance(v, list | tuple):
                for i, j in v:
                    self.choices_keys += [i]
            else:
                self.choices_keys += [k]
        super().__init__(encoder, decoder, **kwargs)

    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "current": {"type": ["boolean", "null"]},
                        "date": {
                            "type": ["string", "null"],
                            "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
                        },
                        "choices": {
                            "type": "array",
                            "items": {"type": "string", "enum": self.choices_keys},
                        },
                        "area": {"type": ["number", "null"]},
                        "yield": {"type": ["number", "null"]},
                        "export": {"type": ["number", "null"]},
                    },
                },
            }
        )
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value


class JSONLeaseField(JSONField):
    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "current": {"type": ["boolean", "null"]},
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
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value


class JSONJobsField(JSONField):
    def _validate_schema(self, value):
        schema = compile(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "current": {"type": ["boolean", "null"]},
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
        try:
            schema(value)
        except JsonSchemaException as e:
            raise ValidationError(e, code="invalid")

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            self._validate_schema(value)
        return value
