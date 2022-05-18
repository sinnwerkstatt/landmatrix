from typing import Any

from django.utils import translation
from graphql import GraphQLResolveInfo
from wagtail.core.models import Site

from apps.graphql.tools import get_fields
from apps.landmatrix.models import Country, Region, Currency
from apps.utils import qs_values_to_dict
from apps.wagtailcms.models import ChartDescriptionsSettings


def resolve_countries(obj: Any, info: GraphQLResolveInfo):
    fields = get_fields(info, recursive=True, exclude=["__typename"])
    return qs_values_to_dict(Country.objects.all(), fields, ["deals"])


def resolve_regions(obj: Any, info: GraphQLResolveInfo):
    fields = get_fields(info, recursive=True, exclude=["__typename"])
    return qs_values_to_dict(Region.objects.all(), fields)


def resolve_currencies(obj: Any, info: GraphQLResolveInfo):
    fields = get_fields(info, recursive=True, exclude=["__typename"])
    return qs_values_to_dict(Currency.objects.all().order_by("name"), fields)


def resolve_chart_descriptions(obj: Any, info: GraphQLResolveInfo, language="en"):
    with translation.override(language):
        site = Site.find_for_request(info.context["request"])
        return ChartDescriptionsSettings.for_site(site).to_dict()
