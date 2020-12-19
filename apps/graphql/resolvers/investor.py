from typing import Any

from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Investor, Deal
from apps.landmatrix.models.gndinvestor import InvestorVersion
from apps.landmatrix.models.versions import Revision
from apps.landmatrix.utils import InvolvementNetwork
from apps.utils import qs_values_to_dict


def resolve_investor(
    obj: Any,
    info: GraphQLResolveInfo,
    id,
    version=None,
    subset="PUBLIC",
    involvements_depth: int = 4,
    involvements_include_ventures: bool = True,
):
    fields = get_fields(info, recursive=True, exclude=["__typename"])

    add_versions = False
    add_deals = False
    add_involvements = False
    filtered_fields = []
    for field in fields:
        if "versions" in field:
            add_versions = True
        elif "deals" in field:
            add_deals = True
        elif "involvements" in field:
            add_involvements = True
        else:
            filtered_fields += [field]

    if version:
        rev = Revision.objects.get(id=version)
        investor = rev.investorversion_set.get().fields
        # investor["involvements"] = [
        #     v.fields for v in rev.investorventureinvolvementversion_set.all()
        # ]
    else:
        visible_investors = Investor.objects.visible(
            info.context["request"].user, subset
        ).filter(id=id)
        if not visible_investors:
            return
        investor = qs_values_to_dict(
            visible_investors,
            filtered_fields,
            ["involvements"],
        )[0]

    if add_versions:
        investor["versions"] = [
            dv.to_dict() for dv in InvestorVersion.objects.filter(object_id=id)
        ]
    if add_deals:
        investor["deals"] = [
            d
            for d in Deal.objects.visible(info.context["request"].user, subset).filter(
                operating_company_id=id
            )
        ]
    if add_involvements:
        investor["involvements"] = InvolvementNetwork(
            involvements_include_ventures
        ).get_network(id, depth=involvements_depth)
    return investor


def resolve_investors(
    obj: Any,
    info: GraphQLResolveInfo,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    qs = Investor.objects.visible(
        user=info.context["request"].user, subset=subset
    ).order_by(sort)

    fields = get_fields(info, recursive=True, exclude=["__typename"])

    if filters:
        qs = qs.filter(parse_filters(filters))

    if limit != 0:
        qs = qs[:limit]

    return qs_values_to_dict(qs, fields, ["involvements", "deals"])


def resolve_investorversions(obj, info: GraphQLResolveInfo, filters=None):
    qs = InvestorVersion.objects.all()
    if filters:
        qs = qs.filter(parse_filters(filters))
    return [iv.to_dict() for iv in qs]
