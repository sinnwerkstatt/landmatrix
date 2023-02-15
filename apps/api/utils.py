from apps.accounts.models import User
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)

from django.contrib.auth import get_user_model


def create_user_lookup() -> dict[int, User]:
    return {user.id: user for user in get_user_model().objects.all()}


def create_country_lookup() -> dict[int, Country]:
    return {country.id: country for country in Country.objects.all()}


def country_to_dict(
    country_id: int | None,
    country_map: dict[int, Country],
):
    if not country_id:
        return
    country = country_map[country_id]
    return {
        "id": country.id,
        "name": country.name,
        "region": {
            "id": country.region.id,
            "name": country.region.name,
        }
        if country.region
        else None,
    }


def user_to_dict(
    user_id: int | None,
    user_map: dict[int, User],
):
    if not user_id:
        return
    user = user_map[user_id]
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
    }


def version_to_dict(
    version: DealVersion | InvestorVersion,
    user_map: dict[int, User],
):
    return {
        "id": version.id,
        "created_at": version.created_at,
        "created_by": user_to_dict(version.created_by_id, user_map),
        "modified_at": version.modified_at,
        "modified_by": user_to_dict(version.modified_by_id, user_map),
    }


def workflowinfo_to_dict(
    wfi: DealWorkflowInfo | InvestorWorkflowInfo,
    user_map: dict[int, User],
):
    is_deal = isinstance(wfi, DealWorkflowInfo)
    return {
        "id": wfi.id,
        "from_user": user_to_dict(wfi.from_user_id, user_map),
        "to_user": user_to_dict(wfi.to_user_id, user_map),
        "draft_status_before": wfi.draft_status_before,
        "draft_status_after": wfi.draft_status_after,
        "obj_version_id": wfi.deal_version_id if is_deal else wfi.investor_version_id,
        "timestamp": wfi.timestamp,
        "comment": wfi.comment or "",
        "resolved": wfi.resolved,
        "replies": wfi.replies or [],
        "__typename": "DealWorkflowInfo" if is_deal else "InvestorWorkflowInfo",
    }


def obj_to_dict(
    obj: Deal | Investor,
    user_map: dict[int, User],
    country_map: dict[int, Country],
):
    last_version = obj.versions.order_by("created_at").last()

    obj_dict = {
        "id": obj.id,
        "country": country_to_dict(obj.country_id, country_map),
        "status": obj.status,
        "draft_status": obj.draft_status,
        "created_at": obj.created_at,
        "created_by": user_to_dict(obj.created_by_id, user_map),
        "workflowinfos": [
            workflowinfo_to_dict(wfi, user_map) for wfi in obj.workflowinfos.all()
        ],
        "modified_at": (
            last_version.modified_at
            if last_version.modified_at
            else last_version.created_at
        ),
        "modified_by": user_to_dict(
            last_version.modified_by_id
            if last_version.modified_by_id
            else last_version.created_by_id,
            user_map,
        ),
    }

    if isinstance(obj, Deal):
        obj_dict["deal_size"] = int(obj.deal_size)
        obj_dict["fully_updated_at"] = obj.fully_updated_at
    else:
        obj_dict["name"] = obj.name
        obj_dict["deals"] = list(obj.deals.order_by("created_at").values("id"))

    return obj_dict
