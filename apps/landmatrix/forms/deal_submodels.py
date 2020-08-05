from django.utils.translation import ugettext as _

from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Location, DataSource, Contract


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
                # {
                #     "name": "file_not_public",
                #     "hidden_in_detail_view": True,
                # TODO: Enable this for editor later.
                # },
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
