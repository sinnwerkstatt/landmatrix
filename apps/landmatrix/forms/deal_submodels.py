from apps.landmatrix.forms import VueForm
from apps.landmatrix.models import Location, DataSource, Contract


class LocationForm(VueForm):
    model = Location


class ContractForm(VueForm):
    model = Contract


class DataSourceForm(VueForm):
    model = DataSource
    attributes = {"file_not_public": {"hidden_in_detail_view": True}}
