location_fields = {
    "id": {"label": "ID", "class": "AutoField", "required": False},
    "name": {
        "label": "Location",
        "class": "TextField",
        "required": False,
    },
    "description": {
        "label": "Description",
        "class": "CharField",
        "required": False,
    },
    "point": {"label": "Point", "class": "PointField", "required": False},
    "facility_name": {
        "label": "Facility name",
        "class": "CharField",
        "required": False,
    },
    "level_of_accuracy": {
        "label": "Spatial accuracy level",
        "class": "CharField",
        "required": False,
        "choices": {
            "COUNTRY": "Country",
            "ADMINISTRATIVE_REGION": "Administrative region",
            "APPROXIMATE_LOCATION": "Approximate location",
            "EXACT_LOCATION": "Exact location",
            "COORDINATES": "Coordinates",
        },
    },
    "comment": {
        "label": "Comment",
        "class": "TextField",
        "required": False,
    },
    "areas": {"label": "Areas", "class": "JSONField", "required": False},
    "deal": {
        "label": "Deal",
        "class": "ForeignKey",
        "required": True,
        "related_model": "Deal",
    },
    "old_group_id": {
        "label": "Old group id",
        "class": "IntegerField",
        "required": False,
    },
}


contract_fields = {
    "id": {"label": "ID", "class": "AutoField", "required": False},
    "old_group_id": {"label": "", "class": "IntegerField", "required": False},
    "number": {"label": "Contract number", "class": "CharField", "required": False},
    "date": {"label": "Date", "class": "DateField", "required": False},
    "expiration_date": {
        "label": "Expiration date",
        "class": "DateField",
        "required": False,
    },
    "agreement_duration": {
        "label": "Duration of the agreement (in years)",
        "class": "IntegerField",
        "required": False,
    },
    "comment": {
        "label": "Comment on contract",
        "class": "TextField",
        "required": False,
    },
}


datasource_fields = {
    "id": {"label": "ID", "class": "AutoField", "required": False},
    "type": {
        "label": "Type",
        "class": "CharField",
        "required": False,
        "choices": {
            "MEDIA_REPORT": "Media report",
            "RESEARCH_PAPER_OR_POLICY_REPORT": "Research Paper / Policy Report",
            "GOVERNMENT_SOURCES": "Government sources",
            "COMPANY_SOURCES": "Company sources",
            "CONTRACT": "Contract",
            "CONTRACT_FARMING_AGREEMENT": "Contract (contract farming agreement)",
            "PERSONAL_INFORMATION": "Personal information",
            "CROWDSOURCING": "Crowdsourcing",
            "OTHER": "Other (Please specify in comment field)",
        },
    },
    "url": {
        "label": "Url",
        "class": "URLField",
        "required": False,
        "type": "url",
    },
    "file": {
        "label": "File",
        "class": "FileField",
        "required": False,
        "help_text": "Maximum file size: 10MB",
    },
    "file_not_public": {
        "label": "Keep PDF not public",
        "class": "BooleanField",
        "required": True,
    },
    "publication_title": {
        "label": "Publication title",
        "class": "CharField",
        "required": False,
    },
    "date": {"label": "Date", "class": "DateField", "required": False},
    "name": {"label": "Name", "class": "CharField", "required": False},
    "company": {
        "label": "Organisation",
        "class": "CharField",
        "required": False,
    },
    "email": {"label": "Email", "class": "EmailField", "required": False},
    "phone": {"label": "Phone", "class": "CharField", "required": False},
    "includes_in_country_verified_information": {
        "label": "Includes in-country-verified information",
        "class": "NullBooleanField",
        "required": False,
    },
    "open_land_contracts_id": {
        "label": "Open Contracting ID",
        "class": "OCIDField",
        "required": False,
    },
    "comment": {
        "label": "Comment on data source",
        "class": "TextField",
        "required": False,
    },
    "deal": {
        "label": "Deal",
        "class": "ForeignKey",
        "required": True,
        "related_model": "Deal",
    },
    "old_group_id": {
        "label": "Old group id",
        "class": "IntegerField",
        "required": False,
    },
}
