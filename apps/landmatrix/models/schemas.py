from fastjsonschema import compile

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
                "pattern": r"^\d{4}(-(0?[1-9]|1[012]))?(-(0?[1-9]|[12][0-9]|3[01]))?$",
            },
            "expiration_date": {
                "type": ["string", "null"],
                "pattern": r"^\d{4}(-(0?[1-9]|1[012]))?(-(0?[1-9]|[12][0-9]|3[01]))?$",
            },
            "agreement_duration": {"type": ["integer", "null"]},
            "comment": {"type": "string"},
        },
    },
}

contracts_schema = compile(contracts_schema_def)


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
                "type": "string",
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
            # TODO Note: data quality too bad at the moment
            # "url": {
            #     "type": "string",
            #     "oneOf": [{"enum": [""]}, {"format": "iri-reference"}],
            # },
            "url": {"type": "string"},
            "file": {"type": ["string", "null"]},
            "file_not_public": {"type": "boolean"},
            "publication_title": {"type": "string"},
            # "date": {"type": ["string", "null"], "format": "date"},
            "date": {
                "type": ["string", "null"],
                "pattern": r"^\d{4}(-(0?[1-9]|1[012]))?(-(0?[1-9]|[12][0-9]|3[01]))?$",
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
