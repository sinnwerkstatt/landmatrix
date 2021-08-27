from typing import Any

from graphql import GraphQLResolveInfo, GraphQLError

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Investor, Deal
from apps.landmatrix.models.gndinvestor import (
    InvestorVersion,
    InvestorWorkflowInfo,
    InvestorVentureInvolvement,
)
from apps.landmatrix.utils import InvolvementNetwork
from apps.utils import qs_values_to_dict
from .generics import (
    add_object_comment,
    change_object_status,
    object_edit,
    object_delete,
)
from .user_utils import get_user_role


def resolve_investor(
    obj: Any,
    info: GraphQLResolveInfo,
    id,
    version=None,
    subset="PUBLIC",
    involvements_depth: int = 4,
    involvements_include_ventures: bool = True,
):
    user = info.context["request"].user
    role = get_user_role(user)

    fields = get_fields(info, recursive=True, exclude=["__typename"])

    add_versions = False
    add_deals = False
    add_workflowinfos = False
    add_involvements = False
    filtered_fields = []
    for field in fields:
        if "versions" in field:
            add_versions = True
        elif "workflowinfos" in field:
            add_workflowinfos = True
        elif "deals" in field:
            add_deals = True
        elif "involvements" in field:
            add_involvements = True
        else:
            filtered_fields += [field]

    if version:
        try:
            investor_version = InvestorVersion.objects.get(id=version)
            investor = investor_version.enriched_dict()
        except InvestorVersion.DoesNotExist:
            return

        if not (
            investor_version.created_by == user or role in ["ADMINISTRATOR", "EDITOR"]
        ):
            raise GraphQLError("not authorized")
        if any([f.startswith("ventures_") for f in fields]):
            investor["ventures"] = InvestorVentureInvolvement.objects.filter(
                investor_id=id
            )
    else:
        visible_investors = Investor.objects.visible(user, subset).filter(id=id)
        if not visible_investors:
            raise GraphQLError("not found")

        investor = qs_values_to_dict(
            visible_investors,
            filtered_fields,
            ["involvements", "investors", "ventures", "workflowinfos"],
        )[0]

    if add_versions:
        investor["versions"] = [
            dv.new_to_dict() for dv in InvestorVersion.objects.filter(object_id=id)
        ]
    if add_workflowinfos:
        investor["workflowinfos"] = [
            dwi.to_dict()
            for dwi in InvestorWorkflowInfo.objects.filter(investor_id=id).order_by(
                "-timestamp"
            )
        ]
    if add_deals:
        investor["deals"] = (
            Deal.objects.visible(info.context["request"].user, subset)
            .filter(operating_company_id=id)
            .order_by("id")
        )

    if add_involvements and not version:
        investor["involvements"] = InvolvementNetwork(
            involvements_include_ventures, max_depth=involvements_depth
        ).get_network(id)

    if investor.get("investors") is None:
        investor["investors"] = []
    if investor.get("ventures") is None:
        investor["ventures"] = []

    return investor


def resolve_investors(
    obj: Any,
    info: GraphQLResolveInfo,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    user = info.context["request"].user
    qs = Investor.objects.visible(user=user, subset=subset).order_by(sort)

    fields = get_fields(info, recursive=True, exclude=["__typename"])
    if any(["involvements" in field for field in fields]):
        raise GraphQLError(
            "Querying involvements via multiple operating companies is too"
            " resource intensive. Please use single investor queries for this."
        )

    qs = qs.filter(parse_filters(filters)) if filters else qs

    qs = qs[:limit] if limit != 0 else qs

    return qs_values_to_dict(
        qs, fields, ["involvements", "ventures", "investors", "deals", "workflowinfos"]
    )


def resolve_investorversions(obj, info: GraphQLResolveInfo, filters=None):
    qs = InvestorVersion.objects.all()
    if filters:
        qs = qs.filter(parse_filters(filters))
    return [iv.to_dict() for iv in qs]


def resolve_add_investor_comment(
    _, info, id: int, version: int, comment: str, to_user_id=None
) -> dict:
    add_object_comment(
        "investor", info.context["request"].user, id, version, comment, to_user_id
    )

    return {"investorId": id, "investorVersion": version}


def resolve_change_investor_status(
    _,
    info,
    id: int,
    version: int,
    transition: str,
    comment: str = None,
    to_user_id: int = None,
) -> dict:
    investorId, investorVersion = change_object_status(
        otype="investor",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        transition=transition,
        comment=comment,
        to_user_id=to_user_id,
    )
    return {"investorId": investorId, "investorVersion": investorVersion}


def resolve_investor_edit(_, info, id, version=None, payload: dict = None) -> dict:
    investorId, investorVersion = object_edit(
        otype="investor",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        payload=payload,
    )
    return {"investorId": investorId, "investorVersion": investorVersion}


def resolve_investor_delete(
    _, info, id: int, version: int = None, comment: str = None
) -> bool:
    return object_delete(
        otype="investor",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        comment=comment,
    )
