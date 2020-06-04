from typing import Any

from ariadne import ObjectType
from django.db.models import Q
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields, parse_filters
from apps.greennewdeal.models import Investor, InvestorVentureInvolvement


def _resolve_investors_prefetching(info: GraphQLResolveInfo):
    qs = Investor.objects.visible(info.context.user)

    # default filters
    default_filters = {"status__in": (2, 3)}
    qs = qs.filter(**default_filters)

    fields = get_fields(info)
    if "country" in fields:
        qs = qs.prefetch_related("country")
    return qs


def resolve_investor(obj: Any, info: GraphQLResolveInfo, id):
    investor = _resolve_investors_prefetching(info)
    return investor.get(id=id)


def resolve_investors(obj, info: GraphQLResolveInfo, filters=None, sort="id", limit=20):
    qs = _resolve_investors_prefetching(info).order_by(sort)
    if filters:
        qs = qs.filter(**parse_filters(filters))

    # limit = max(1, min(limit, 500))
    if limit != 0:
        qs = qs[:limit]
    return qs


investor_type = ObjectType("Investor")
investor_type.set_field("deals", lambda obj, info: obj.deals.all())


@investor_type.field("involvements")
def get_investor_involvements(obj, info: GraphQLResolveInfo):
    involves = InvestorVentureInvolvement.objects.visible(info.context.user)

    involves = involves.filter(Q(investor=obj) | Q(venture=obj))
    involves = involves.filter(investor__status__in=(2, 3)).filter(
        venture__status__in=(2, 3)
    )

    return involves


def resolve_involvements(
    obj, info: GraphQLResolveInfo, filters=None, sort="id", limit=20
):
    qs = InvestorVentureInvolvement.objects.visible(info.context.user)

    # default filters
    default_filters = {"status__in": (2, 3)}
    qs = qs.filter(**default_filters).order_by(sort)

    if filters:
        qs = qs.filter(**parse_filters(filters))
    if limit != 0:
        qs = qs[:limit]
    return qs
