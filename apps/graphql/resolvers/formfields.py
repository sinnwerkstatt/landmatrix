from django.utils import translation

from apps.landmatrix.forms.deal import DealForm
from apps.landmatrix.forms.deal_submodels import (
    contract_fields,
    location_fields,
    datasource_fields,
)
from apps.landmatrix.forms.investor import InvestorVentureInvolvementForm, InvestorForm


def resolve_formfields(_obj, _info, language="en"):
    with translation.override(language):
        return {
            "deal": DealForm().as_json(),
            "location": location_fields,
            "contract": contract_fields,
            "datasource": datasource_fields,
            "investor": InvestorForm().as_json(),
            "involvement": InvestorVentureInvolvementForm().as_json(),
        }
