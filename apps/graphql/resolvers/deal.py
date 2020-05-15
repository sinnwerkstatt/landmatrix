from typing import Any

from ariadne import ObjectType
from django.contrib.auth.models import User
from django.db.models import Sum
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields, parse_filters
from apps.greennewdeal.models import Deal, Location


def _resolve_deals_prefetching(info: GraphQLResolveInfo):
    qs = Deal.objects

    # default filters
    user: User = info.context.user
    if user.is_staff or user.is_superuser:
        # TODO: apply default filters if nothing else is set.
        default_filters = {"status__in": (2, 3), "confidential": False}
        qs = qs.filter(**default_filters)
    else:
        default_filters = {"status__in": (2, 3), "confidential": False}
        qs = qs.filter(**default_filters)

    fields = get_fields(info)
    if "target_country" in fields:
        qs = qs.prefetch_related("target_country")
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


def resolve_locations(obj, info: GraphQLResolveInfo, filters=None, limit=20):
    qs = Location.objects.all()

    # default filters
    qs = qs.filter(deal__status__in=(2, 3), deal__confidential=False)

    fields = get_fields(info)
    if "deal" in fields:
        qs = qs.select_related("deal")

    if filters:
        qs = qs.filter(**parse_filters(filters))

    if limit != 0:
        qs = qs[:limit]
    return qs


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    from apps.greennewdeal.models import Deal

    size = sum([d.get_deal_size() for d in Deal.objects.filter(status__in=[2, 3])])
    deal_count = Deal.objects.filter(status__in=[2, 3]).count()

    neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))
