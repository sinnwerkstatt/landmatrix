from django.utils import translation
from wagtail.core.models import Site

from apps.graphql.tools import get_fields
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.deal import Deal
from apps.utils import qs_values_to_dict
from apps.wagtailcms.models import ChartDescriptionsSettings


def resolve_countries(_obj, info):
    fields = get_fields(info, recursive=True, exclude=["__typename"])
    return qs_values_to_dict(Country.objects.all(), fields, ["deals"])


def resolve_regions(_obj, info):
    fields = get_fields(info, recursive=True, exclude=["__typename"])
    return qs_values_to_dict(Region.objects.all(), fields)


def resolve_currencies(_obj, info):
    fields = get_fields(info, recursive=True, exclude=["__typename"])
    return qs_values_to_dict(Currency.objects.all().order_by("name"), fields)


def resolve_chart_descriptions(_obj, info, language="en"):
    with translation.override(language):
        site = Site.find_for_request(info.context["request"])
        return ChartDescriptionsSettings.for_site(site).to_dict()


def resolve_markers(_obj, _info, region_id=None, country_id=None):
    return Deal.get_geo_markers(region_id, country_id)
