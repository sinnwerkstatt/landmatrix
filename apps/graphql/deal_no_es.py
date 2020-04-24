from typing import Any

from django.db.models import Sum
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields
from apps.greennewdeal.models import Deal, Location


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


def resolve_locations(obj: Any, info: GraphQLResolveInfo, sort="id", limit=20):
    locations = Location.objects.all()  # .filter(deal__status__in=(2, 3))
    # fields = get_fields(info)
    location_dict = []
    for location in locations.values():
        loc = location
        if location["point"]:
            lon, lat = location["point"]
            loc["point"] = {"lat": lat, "lon": lon}
        else:
            del loc["point"]
        loc["deal"] = {"id": location["deal_id"]}
        location_dict += [loc]
    return location_dict


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    from apps.greennewdeal.models import Deal

    size = sum([d.get_deal_size() for d in Deal.objects.filter(status__in=[2, 3])])
    deal_count = Deal.objects.filter(status__in=[2, 3]).count()

    neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))
