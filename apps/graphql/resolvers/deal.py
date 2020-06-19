from typing import Any

from ariadne import ObjectType
from django.db.models import Sum
from graphql import GraphQLResolveInfo
from reversion.models import Version

from apps.graphql.tools import get_fields, parse_filters
from apps.greennewdeal.models import Deal, Location


def _resolve_deals_prefetching(info: GraphQLResolveInfo):
    qs = Deal.objects.visible(info.context.user)

    fields = get_fields(info)
    if "country" in fields:
        qs = qs.prefetch_related("country")
    if "locations" in fields:
        qs = qs.prefetch_related("locations")
    if "contracts" in fields:
        qs = qs.prefetch_related("contracts")
    if "datasources" in fields:
        qs = qs.prefetch_related("datasources")
    return qs


def resolve_deal(obj, info: GraphQLResolveInfo, id):
    deal = _resolve_deals_prefetching(info)
    return deal.get(id=id)


def resolve_deals(
    obj, info: GraphQLResolveInfo, filters=None, sort="id", limit=20, after=None
):
    qs = _resolve_deals_prefetching(info).order_by(sort)
    if filters:
        qs = qs.filter(**parse_filters(filters))

    if after:
        qs = qs.filter(**{f"{sort}__gt": after})

    # limit = max(1, min(limit, 500))
    if limit != 0:
        qs = qs[:limit]
    return qs


deal_type = ObjectType("Deal")
deal_type.set_field("locations", lambda obj, info: obj.locations.all())
deal_type.set_field("datasources", lambda obj, info: obj.datasources.all())
deal_type.set_field("contracts", lambda obj, info: obj.contracts.all())


@deal_type.field("reversions")
def get_deal_reversions(obj, info: GraphQLResolveInfo):
    versions = Version.objects.get_for_object(obj, model_db=None)
    return [x.field_dict for x in versions]


def resolve_locations(obj, info: GraphQLResolveInfo, filters=None, limit=20):
    qs = Location.objects.visible(info.context.user)

    fields = get_fields(info)
    if "deal" in fields:
        qs = qs.select_related("deal")

    if filters:
        qs = qs.filter(**parse_filters(filters))

    if limit != 0:
        qs = qs[:limit]
    return qs


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))
