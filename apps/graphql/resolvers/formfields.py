from django.utils import translation

from apps.landmatrix.forms.deal import DealForm
from apps.landmatrix.forms.deal_submodels import get_submodels_fields
from apps.landmatrix.forms.investor import InvestorForm, InvestorVentureInvolvementForm


def resolve_formfields(_obj, _info, language="en"):
    with translation.override(language):
        return {
            "deal": DealForm().as_json(),
            **get_submodels_fields(),
            "investor": InvestorForm().as_json(),
            "involvement": InvestorVentureInvolvementForm().as_json(),
        }
