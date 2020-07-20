from django.utils.translation import ugettext as _

from apps.greennewdeal.forms import VueForm
from apps.greennewdeal.models import Deal, Location, DataSource, Contract


class LocationForm(VueForm):
    model = Location
    sections = {
        "general_info": {
            "label": _("Location"),
            "fields": [
                "name",
                "description",
                "point",
                "facility_name",
                "level_of_accuracy",
                "comment",
            ],
        }
    }


class ContractForm(VueForm):
    model = Contract
    sections = {
        "general_info": {
            "label": _("Contract"),
            "fields": [
                "number",
                "date",
                "expiration_date",
                "agreement_duration",
                "comment",
            ],
        }
    }


class DataSourceForm(VueForm):
    model = DataSource
    sections = {
        "general_info": {
            "label": _("Data source"),
            "fields": [
                "type",
                "url",
                "file",
                "file_not_public",
                "publication_title",
                "date",
                "name",
                "company",
                "email",
                "phone",
                "includes_in_country_verified_information",
                "open_land_contracts_id",
                "comment",
            ],
        }
    }
