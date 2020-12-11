from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Investor
from apps.landmatrix.models.gndinvestor import InvestorVersion
from apps.landmatrix.utils import InvolvementNetwork


def resolve_investor(obj: Any, info: GraphQLResolveInfo, id):
    try:
        return Investor.objects.visible(info.context.user, "UNFILTERED").get(id=id)
    except Investor.DoesNotExist:
        return


def resolve_investors(
    obj: Any,
    info: GraphQLResolveInfo,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    qs = Investor.objects.visible(user=info.context.user, subset=subset).order_by(sort)

    fields = get_fields(info)
    if "country" in fields:
        qs = qs.prefetch_related("country")
    if "deals" in fields:
        qs = qs.prefetch_related("deals")

    if filters:
        qs = qs.filter(parse_filters(filters))

    if limit != 0:
        qs = qs[:limit]
    return qs


investor_type = ObjectType("Investor")
investor_type.set_field("deals", lambda obj, info: obj.deals.all())
investor_type.set_field(
    "versions",
    lambda obj, info: [
        dv.to_dict() for dv in InvestorVersion.objects.filter(object_id=obj.id)
    ],
)


def resolve_investorversions(obj, info: GraphQLResolveInfo, filters=None):
    qs = InvestorVersion.objects.all()
    if filters:
        qs = qs.filter(parse_filters(filters))
    return [iv.to_dict() for iv in qs]


@investor_type.field("involvements")
def resolve_involvements_network(
    obj: Any, info: GraphQLResolveInfo, depth, include_ventures=True
):
    investors = InvolvementNetwork(include_ventures=include_ventures).get_network(
        obj.id, depth=depth
    )
    # print(dict(investors))
    return investors


# i think we dont need this either.
# def resolve_involvements(
#     obj, info: GraphQLResolveInfo, filters=None, limit=20
# ):
#     qs = InvestorVentureInvolvement.objects.visible(info.context.user)
#
#     if filters:
#         qs = qs.filter(parse_filters(filters))
#     if limit != 0:
#         qs = qs[:limit]
#     return qs
