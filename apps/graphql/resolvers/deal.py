from ariadne.graphql import GraphQLError

from django.contrib.gis.geos import Point

from apps.accounts.models import UserRole
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.utils import qs_values_to_dict, set_sensible_fields_to_null
from .generics import (
    add_object_comment,
    change_object_status,
    get_foreign_keys,
    object_edit,
)
from ..tools import get_fields, parse_filters


def resolve_deal(_obj, info, id, version=None, subset="PUBLIC"):
    if not user.is_authenticated:
        set_sensible_fields_to_null(deal)

    return deal


def resolve_deals(_obj, info):
    if not user.is_authenticated:
        set_sensible_fields_to_null(results)

    return results


def resolve_add_deal_comment(
    _obj, info, id: int, version: int, comment: str, to_user_id=None
) -> dict:
    add_object_comment(
        "deal", info.context["request"].user, id, version, comment, to_user_id
    )

    return {"dealId": id, "dealVersion": version}


# noinspection PyShadowingBuiltins
def resolve_change_deal_status(
    _obj,
    info,
    id: int,
    version: int,
    transition: str,
    comment: str | None = None,
    to_user_id: int | None = None,
    fully_updated: bool = False,  # only relevant on "TO_REVIEW"
) -> dict:
    deal_id, deal_version = change_object_status(
        otype="deal",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        transition=transition,
        comment=comment,
        to_user_id=to_user_id,
        fully_updated=fully_updated,
    )
    return {"dealId": deal_id, "dealVersion": deal_version}


def _clean_payload(payload: dict | None) -> dict:
    ret: dict = {}

    if payload is None:
        return ret

    foreign_keys = get_foreign_keys(Deal)

    for key, value in payload.items():
        if key in foreign_keys:
            if value:
                ret[key] = foreign_keys[key].objects.get(id=value["id"])
        elif key == "point":
            ret["point"] = Point(value["lng"], value["lat"])
        elif key in ["locations", "datasources", "contracts"]:
            new_value = [
                val for val in value if any([v for k, v in val.items() if k != "id"])
            ]
            ret[key] = new_value
        else:
            ret[key] = value
    return ret


# noinspection PyShadowingBuiltins
def resolve_deal_edit(
    _obj,
    info,
    id: int,
    version: int | None = None,
    payload: dict | None = None,
) -> dict:
    deal_id, deal_version = object_edit(
        otype="deal",
        user=info.context["request"].user,
        obj_id=id,
        obj_version_id=version,
        payload=_clean_payload(payload),
    )
    return {"dealId": deal_id, "dealVersion": deal_version}
