from typing import Any

from django.db.models import Sum
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields
from apps.greennewdeal.models import Deal


def do_deals(obj: Any, info: GraphQLResolveInfo):
    deals = Deal.objects.filter(status__in=(2, 3))
    fields = get_fields(info)
    if "locations" in fields:
        deals = deals.prefetch_related("locations")
    #         deals = deals.prefetch_related("locations")
    #     deals = deals.values()
    # deal_list = []
    # for deal in deals:
    #     locations = [location for location in deal.locations.all()]
    #
    #     deal.locations = locations
    #     deal_list += [deal]
    return deals


def resolve_deal(obj: Any, info: GraphQLResolveInfo, id):
    deal = do_deals(obj, info).get(id=id)
    return deal


def resolve_deals(obj: Any, info: GraphQLResolveInfo, sort="id", limit=20):
    deals = do_deals(obj, info).order_by(sort)
    limit = max(1, min(limit, 500))
    deals = deals[:limit]
    return deals


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    from apps.greennewdeal.models import Deal

    size = sum([d.get_deal_size() for d in Deal.objects.filter(status__in=[2, 3])])
    deal_count = Deal.objects.filter(status__in=[2, 3]).count()

    neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))
