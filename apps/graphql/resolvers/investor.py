from ariadne.graphql import GraphQLError

from apps.accounts.models import UserRole
from apps.landmatrix.models.deal import Deal
from apps.landmatrix.models.investor import (
    Investor,
    InvestorVentureInvolvement,
    InvestorVersion,
    InvestorWorkflowInfo,
)
from apps.landmatrix.utils import InvolvementNetwork
from apps.utils import qs_values_to_dict

from ..tools import get_fields, parse_filters
from .generics import (
    add_object_comment,
    change_object_status,
    get_foreign_keys,
    object_delete,
    object_edit,
)


# noinspection PyShadowingBuiltins
def resolve_investor(
    _obj,
    info,
    id,
    version=None,
    subset="PUBLIC",
    involvements_depth: int = 4,
    involvements_include_ventures: bool = True,
) -> dict | None:
    user = info.context["request"].user

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
            return None

        if not any(
            [
                user.is_authenticated and user.role >= UserRole.EDITOR,
                investor_version.created_by == user,
                investor_version.serialized_data["draft_status"] is None
                and investor_version.serialized_data["status"] in [2, 3],
            ]
        ):
            raise GraphQLError("MISSING_AUTHORIZATION")
        if any([f.startswith("ventures_") for f in fields]):
            investor["ventures"] = InvestorVentureInvolvement.objects.filter(
                investor_id=id
            )
    else:
        visible_investors = Investor.objects.visible(user, subset).filter(id=id)
        if not visible_investors:
            raise GraphQLError("INVESTOR_NOT_FOUND")

        investor = qs_values_to_dict(
            visible_investors,
            filtered_fields,
            ["involvements", "investors", "ventures", "workflowinfos"],
        )[0]

    if add_versions:
        investor["versions"] = [
            dv.to_dict() for dv in InvestorVersion.objects.filter(object_id=id)
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
    _obj,
    info,
    sort="id",
    limit=20,
    subset="PUBLIC",
    filters=None,
):
    if not limit:
        limit = 20

    user = info.context["request"].user
    qs = Investor.objects.visible(user=user, subset=subset).order_by(sort)

    fields = get_fields(info, recursive=True, exclude=["__typename"])
    if any(["involvements" in field for field in fields]):
        raise GraphQLError(
            "Querying involvements via multiple operating companies is too"
            " resource intensive. Please use single investor queries for this."
        )

    qs = qs.filter(parse_filters(filters)) if filters else qs

    qs = qs.filter(id__in=qs[:limit].values("id"))

    return qs_values_to_dict(
        qs, fields, ["involvements", "ventures", "investors", "deals", "workflowinfos"]
    )


def resolve_investorversions(_obj, _info, filters=None):
    qs = InvestorVersion.objects.all()
    if filters:
        qs = qs.filter(parse_filters(filters))
    return [iv.to_dict() for iv in qs]


# noinspection PyShadowingBuiltins
def resolve_add_investor_comment(
    _obj, info, id: int, version: int, comment: str, to_user_id=None
) -> dict:
    add_object_comment(
        "investor", info.context["request"].user, id, version, comment, to_user_id
    )

    return {"investorId": id, "investorVersion": version}


# noinspection PyShadowingBuiltins
def resolve_change_investor_status(
    _obj,
    info,
    id: int,
    version: int,
    transition: str,
    comment: str | None = None,
    to_user_id: int | None = None,
) -> dict:
    investor_id, investor_version = change_object_status(
        otype="investor",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        transition=transition,
        comment=comment,
        to_user_id=to_user_id,
    )
    return {"investorId": investor_id, "investorVersion": investor_version}


def _clean_payload(payload: dict | None, investor_id: int) -> dict:
    ret: dict = {}

    if payload is None:
        return ret

    foreign_keys = get_foreign_keys(Investor)

    for key, value in payload.items():
        if key in foreign_keys and value:
            ret[key] = foreign_keys[key].objects.get(id=value["id"])
        elif key == "datasources" and value:
            ret[key] = [
                val for val in value if any([v for k, v in val.items() if k != "id"])
            ]
        elif key == "investors":
            ivis = []
            for entry in value:
                ivi = InvestorVentureInvolvement()
                if ivi_id := entry.get("id"):
                    try:
                        ivi = InvestorVentureInvolvement.objects.get(id=ivi_id)
                    except (ValueError, InvestorVentureInvolvement.DoesNotExist):
                        pass  # it's okay, we'll use the new instance
                ivi.venture_id = investor_id
                ivi.investor_id = entry["investor"]["id"]
                ivi.role = entry["role"]
                ivi.investment_type = entry.get("investment_type")
                ivi.percentage = entry.get("percentage")
                ivi.loans_amount = entry.get("loans_amount")
                ivi.loans_currency_id = (
                    entry["loans_currency"]["id"]
                    if entry.get("loans_currency")
                    else None
                )
                ivi.loans_date = entry.get("loans_date", "")
                ivi.parent_relation = entry.get("parent_relation")
                ivi.comment = entry.get("comment", "")
                ivis += [ivi]
            ret["_investors"] = ivis
        else:
            ret[key] = value
    return ret


# noinspection PyShadowingBuiltins
def resolve_investor_edit(
    _obj,
    info,
    id: int,
    version: int | None = None,
    payload: dict | None = None,
) -> dict:
    investor_id, investor_version = object_edit(
        otype="investor",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        payload=_clean_payload(payload, investor_id=id),
    )
    return {"investorId": investor_id, "investorVersion": investor_version}


# noinspection PyShadowingBuiltins
def resolve_investor_delete(
    _obj,
    info,
    id: int,
    version: int | None = None,
    comment: str | None = None,
) -> bool:
    return object_delete(
        otype="investor",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        comment=comment,
    )
