from typing import Any

from django.utils import translation
from graphql import GraphQLResolveInfo

from apps.landmatrix.forms.deal import DealFrontendForm
from apps.landmatrix.forms.deal_submodels import (
    contract_fields,
    location_fields,
    datasource_fields,
)
from apps.landmatrix.forms.investor import (
    InvestorFrontendForm,
    InvestorVentureInvolvementForm,
)


def resolve_formfields(obj: Any, info: GraphQLResolveInfo, language="en"):
    with translation.override(language):
        return {
            "deal": DealFrontendForm().get_fields(),
            "location": location_fields,
            "contract": contract_fields,
            "datasource": datasource_fields,
            "investor": InvestorFrontendForm().get_fields(),
            "involvement": InvestorVentureInvolvementForm().get_fields(),
        }
