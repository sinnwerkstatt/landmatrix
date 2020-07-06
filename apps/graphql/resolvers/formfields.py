from typing import Any

from django.utils import translation
from graphql import GraphQLResolveInfo

from apps.greennewdeal.forms.deal import DealForm


def resolve_formfields(obj: Any, info: GraphQLResolveInfo, language="en"):
    with translation.override(language):
        return {"deal": (DealForm().get_fields())}
