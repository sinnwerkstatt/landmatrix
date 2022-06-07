from django.utils.translation import gettext as _

location_fields = {
    "id": {"label": "ID", "class": "NanoIDField"},
    "name": {"label": _("Location"), "class": "CharField"},
    "description": {"label": _("Description"), "class": "TextField"},
    "point": {"label": _("Point"), "class": "PointField"},
    "facility_name": {"label": _("Facility name"), "class": "CharField"},
    "level_of_accuracy": {
        "label": _("Spatial accuracy level"),
        "class": "TypedChoiceField",
        "choices": {
            "COUNTRY": _("Country"),
            "ADMINISTRATIVE_REGION": _("Administrative region"),
            "APPROXIMATE_LOCATION": _("Approximate location"),
            "EXACT_LOCATION": _("Exact location"),
            "COORDINATES": _("Coordinates"),
        },
    },
    "comment": {"label": _("Comment"), "class": "TextField"},
    "areas": {"label": _("Areas"), "class": "JSONField"},
    "deal": {
        "label": _("Deal"),
        "class": "ForeignKey",
        "required": True,
        "related_model": "Deal",
    },
}


contract_fields = {
    "id": {"label": "ID", "class": "NanoIDField"},
    "number": {"label": _("Contract number"), "class": "CharField"},
    "date": {"label": _("Date"), "class": "DateField"},
    "expiration_date": {"label": _("Expiration date"), "class": "DateField"},
    "agreement_duration": {
        "label": _("Duration of the agreement"),
        "class": "IntegerField",
        "unit": _("years"),
    },
    "comment": {"label": _("Comment on contract"), "class": "TextField"},
    "deal": {
        "label": _("Deal"),
        "class": "ForeignKey",
        "required": True,
        "related_model": "Deal",
    },
}


datasource_fields = {
    "id": {"label": "ID", "class": "NanoIDField"},
    "type": {
        "label": _("Type"),
        "class": "TypedChoiceField",
        "choices": {
            "": "--------",
            "MEDIA_REPORT": _("Media report"),
            "RESEARCH_PAPER_OR_POLICY_REPORT": _("Research Paper / Policy Report"),
            "GOVERNMENT_SOURCES": _("Government sources"),
            "COMPANY_SOURCES": _("Company sources"),
            "CONTRACT": "Contract",
            "CONTRACT_FARMING_AGREEMENT": _("Contract (contract farming agreement)"),
            "PERSONAL_INFORMATION": _("Personal information"),
            "CROWDSOURCING": _("Crowdsourcing"),
            "OTHER": _("Other (Please specify in comment field)"),
        },
    },
    "url": {"label": _("Url"), "class": "URLField", "type": "url"},
    "file": {"label": _("File"), "class": "FileField"},
    "file_not_public": {"label": _("Keep PDF not public"), "class": "BooleanField"},
    "publication_title": {"label": _("Publication title"), "class": "CharField"},
    "date": {"label": _("Date"), "class": "DateField"},
    "name": {"label": _("Name"), "class": "CharField"},
    "company": {"label": _("Organisation"), "class": "CharField"},
    "email": {"label": _("Email"), "class": "EmailField"},
    "phone": {"label": _("Phone"), "class": "CharField"},
    "includes_in_country_verified_information": {
        "label": _("Includes in-country-verified information"),
        "class": "NullBooleanField",
    },
    "open_land_contracts_id": {"label": _("Open Contracting ID"), "class": "OCIDField"},
    "comment": {"label": _("Comment on data source"), "class": "TextField"},
    "deal": {
        "label": _("Deal"),
        "class": "ForeignKey",
        "required": True,
        "related_model": "Deal",
    },
}
