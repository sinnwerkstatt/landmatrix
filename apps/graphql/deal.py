from typing import Any

from ariadne import ObjectType
from django.db.models import Sum
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields
from apps.greennewdeal.models import Deal, Location


def _resolve_deals_prefetching(obj: Any, info: GraphQLResolveInfo):
    deals = Deal.objects.filter(status__in=(2, 3))
    fields = get_fields(info)
    if "locations" in fields:
        deals = deals.prefetch_related("locations")
    if "contracts" in fields:
        deals = deals.prefetch_related("contracts")
    if "datasources" in fields:
        deals = deals.prefetch_related("datasources")
    return deals


def resolve_deal(obj: Any, info: GraphQLResolveInfo, id):
    deal = _resolve_deals_prefetching(obj, info)
    return deal.get(id=id)


def resolve_deals(
    obj: Any, info: GraphQLResolveInfo, filters=None, sort="id", limit=20
):
    deals = _resolve_deals_prefetching(obj, info).order_by(sort)
    # limit = max(1, min(limit, 500))
    deals = deals[:limit]
    return deals


deal_type = ObjectType("Deal")
deal_type.set_field("locations", lambda obj, info: obj.locations.all())
deal_type.set_field("datasources", lambda obj, info: obj.datasources.all())
deal_type.set_field("contracts", lambda obj, info: obj.contracts.all())


def resolve_locations(
    obj: Any, info: GraphQLResolveInfo, filters=None, sort="id", limit=20
):
    locations = Location.objects.filter(deal__status__in=(2, 3)).select_related("deal")
    # fields = get_fields(info)
    return locations[:limit]


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    from apps.greennewdeal.models import Deal

    size = sum([d.get_deal_size() for d in Deal.objects.filter(status__in=[2, 3])])
    deal_count = Deal.objects.filter(status__in=[2, 3]).count()

    neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))
