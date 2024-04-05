import json

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from fastjsonschema import JsonSchemaException, compile


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


locations_schema_def = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {
                "anyOf": [
                    {"type": "integer"},
                    {"type": "string", "minLength": 8, "maxLength": 8},
                ]
            },
            "old_id": {"type": ["integer", "null"]},
            "old_group_id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "point": {
                "type": ["object", "null"],
                "properties": {
                    "lat": {"type": "number", "minimum": -90, "maximum": 90},
                    "lng": {"type": "number", "minimum": -180, "maximum": 180},
                },
            },
            "facility_name": {"type": "string"},
            "level_of_accuracy": {
                "type": "string",
                "enum": [
                    "",
                    "COUNTRY",
                    "ADMINISTRATIVE_REGION",
                    "APPROXIMATE_LOCATION",
                    "EXACT_LOCATION",
                    "COORDINATES",
                ],
            },
            "comment": {"type": "string"},
            "areas": {"type": ["object", "null"]},
        },
    },
}
locations_schema = compile(locations_schema_def)


class LocationsField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_definition = locations_schema


contracts_schema_def = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {
                "anyOf": [
                    {"type": "integer"},
                    {"type": "string", "minLength": 8, "maxLength": 8},
                ]
            },
            "old_id": {"type": ["integer", "null"]},
            "old_group_id": {"type": "integer"},
            "number": {"type": "string"},
            "date": {
                "type": ["string", "null"],
                "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
            },
            "expiration_date": {
                "type": ["string", "null"],
                "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
            },
            "agreement_duration": {"type": ["integer", "null"]},
            "comment": {"type": "string"},
        },
    },
}

contracts_schema = compile(contracts_schema_def)


class ContractsField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_definition = contracts_schema


datasources_schema_def = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {
                "anyOf": [
                    {"type": "integer"},
                    {"type": "string", "minLength": 8, "maxLength": 8},
                ]
            },
            "old_id": {"type": ["integer", "null"]},
            "old_group_id": {"type": "integer"},
            "type": {
                "enum": [
                    "",
                    "MEDIA_REPORT",
                    "RESEARCH_PAPER_OR_POLICY_REPORT",
                    "GOVERNMENT_SOURCES",
                    "COMPANY_SOURCES",
                    "CONTRACT",
                    "CONTRACT_FARMING_AGREEMENT",
                    "PERSONAL_INFORMATION",
                    "CROWDSOURCING",
                    "OTHER",
                ],
            },
            "url": {"type": "string"},
            "file": {"type": ["string", "null"]},
            "file_not_public": {"type": "boolean"},
            "publication_title": {"type": "string"},
            # "date": {"type": ["string", "null"], "format": "date"},
            "date": {
                "type": ["string", "null"],
                "pattern": r"^\d{4}(-(0?[1-9]|1[012])(-(0?[1-9]|[12][0-9]|3[01]))?)?$",
            },
            "name": {"type": "string"},
            "company": {"type": "string"},
            # "email": {"type": "string", "oneOf": [{"enum": [""]}, {"format": "email"}]},  # too strict
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "includes_in_country_verified_information": {"type": ["boolean", "null"]},
            "open_land_contracts_id": {"type": "string"},
            "comment": {"type": "string"},
        },
    },
}
datasources_schema = compile(datasources_schema_def)


class DatasourcesField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_definition = datasources_schema
