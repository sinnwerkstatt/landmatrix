from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Location, DataSource, Contract
from django.utils.translation import ugettext as _


class LocationForm(VueForm):
    model = Location
    attributes = {"name": {"label": _("Location")}}
    extra_display_fields = {
        "country": {"class": "CharField", "label": _("Target country")}
    }


class ContractForm(VueForm):
    model = Contract


class DataSourceForm(VueForm):
    model = DataSource
    attributes = {
        "file_not_public": {"hidden_in_detail_view": True},
        "url": {"type": "url"},
        "company": {"label": _("Organisation")},
        "open_land_contracts_id": {"class": "OCIDField"},
    }
