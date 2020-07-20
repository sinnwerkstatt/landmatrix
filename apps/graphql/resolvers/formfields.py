from typing import Any

from django.utils import translation
from graphql import GraphQLResolveInfo

from apps.greennewdeal.forms.deal import DealForm
from apps.greennewdeal.forms.deal_submodels import (
    LocationForm,
    ContractForm,
    DataSourceForm,
)


def resolve_formfields(obj: Any, info: GraphQLResolveInfo, language="en"):
    with translation.override(language):
        return {
            "deal": DealForm().get_fields(),
            "location": LocationForm().get_fields(),
            "contract": ContractForm().get_fields(),
            "datasource": DataSourceForm().get_fields(),
        }
