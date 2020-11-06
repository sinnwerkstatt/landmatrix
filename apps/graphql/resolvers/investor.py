from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from reversion.models import Version

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Investor, InvestorVentureInvolvement, Country
from apps.landmatrix.utils import InvolvementNetwork


def _resolve_investors_prefetching(info: GraphQLResolveInfo):
    qs = Investor.objects.visible(info.context.user)

    fields = get_fields(info)
    if "country" in fields:
        qs = qs.prefetch_related("country")
    if "deals" in fields:
        qs = qs.prefetch_related("deals")
    return qs


def resolve_investor(obj: Any, info: GraphQLResolveInfo, id):
    investor = _resolve_investors_prefetching(info)
    return investor.get(id=id)


def resolve_investors(obj, info: GraphQLResolveInfo, filters=None, sort="id", limit=20):
    qs = _resolve_investors_prefetching(info).order_by(sort)
    if filters:
        qs = qs.filter(parse_filters(filters))

    # limit = max(1, min(limit, 500))
    if limit != 0:
        qs = qs[:limit]
    return qs


investor_type = ObjectType("Investor")
investor_type.set_field("deals", lambda obj, info: obj.deals.all())


def _resolve_field_dict_fetch(field_dict):
    if "country_id" in field_dict and not field_dict["country_id"] is None:
        try:
            c = Country.objects.get(id=field_dict["country_id"])
            field_dict["country"] = c.to_dict(deep=True)
        except Country.DoesNotExist:
            pass

    return field_dict


def resolve_investorversions(obj, info: GraphQLResolveInfo, filters=None):
    qs = Version.objects.get_for_model(Investor)  # .filter(revision__date_created="")
    # qs = _resolve_deals_prefetching(info).order_by(sort)
    if filters:
        qs = qs.filter(parse_filters(filters))

    return [
        {
            "id": x.id,
            "investor": _resolve_field_dict_fetch(x.field_dict),
            "revision": x.revision,
        }
        for x in qs
    ]


@investor_type.field("involvements")
def resolve_involvements_network(
    obj: Any, info: GraphQLResolveInfo, depth, include_ventures=True
):
    investors = InvolvementNetwork(include_ventures=include_ventures).get_network(
        obj.id, depth=depth
    )
    # print(dict(investors))
    return investors


def resolve_involvements(
    obj, info: GraphQLResolveInfo, filters=None, sort="id", limit=20
):
    qs = InvestorVentureInvolvement.objects.visible(info.context.user)

    if filters:
        qs = qs.filter(parse_filters(filters))
    if limit != 0:
        qs = qs[:limit]
    return qs
