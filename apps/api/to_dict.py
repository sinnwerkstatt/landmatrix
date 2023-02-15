from collections.abc import Callable, Iterable
from datetime import datetime
from typing import Type, TypedDict, TypeVar, cast

from django.contrib.auth import get_user_model
from django.db.models import Model

from apps.accounts.models import User
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal, DealWorkflowInfo
from apps.landmatrix.models.investor import Investor, InvestorWorkflowInfo


class UserDict(TypedDict):
    id: int
    username: str
    full_name: str


class RegionDict(TypedDict):
    id: int
    name: str


class CountryDict(TypedDict):
    id: int
    name: str
    region: RegionDict | None


class WFReplyDict(TypedDict):
    timestamp: str
    user_id: int
    comment: str


class WorkflowInfoDict(TypedDict):
    id: int
    comment: str
    from_user: UserDict | None
    to_user: UserDict | None
    draft_status_before: int
    draft_status_after: int
    timestamp: datetime
    resolved: bool
    replies: list[WFReplyDict]
    __typename: str


class BaseObjDict(TypedDict):
    id: int
    country: CountryDict | None
    status: int
    draft_status: int
    created_at: datetime
    created_by: UserDict | None
    modified_at: datetime | None
    modified_by: UserDict | None
    workflowinfos: list[WorkflowInfoDict]


class DealDict(BaseObjDict):
    deal_size: int
    fully_updated_at: datetime | None


class InvestorDict(BaseObjDict):
    name: str
    deals: list[int]


class Lookups(TypedDict):
    user: dict[int, UserDict]
    country: dict[int, CountryDict]


T = TypeVar("T", bound=Model)
V = TypeVar("V")


def create_model_lookup(
    qs: Iterable[T],
    map_fn: Callable[[T], V],
) -> dict[int, V]:
    return {val.id: map_fn(val) for val in qs}


def user_to_dict(user: User) -> UserDict:
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
    }


def country_to_dict(
    country: Country,
) -> CountryDict:
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


def create_lookups() -> Lookups:
    return {
        "user": create_model_lookup(
            get_user_model().objects.all(),
            user_to_dict,
        ),
        "country": create_model_lookup(
            Country.objects.all(),
            country_to_dict,
        ),
    }


def workflowinfo_to_dict(
    wfi: DealWorkflowInfo | InvestorWorkflowInfo,
    lookups: Lookups,
) -> WorkflowInfoDict:
    is_deal = isinstance(wfi, DealWorkflowInfo)
    return {
        "id": wfi.id,
        "from_user": lookups["user"].get(wfi.from_user_id),  # noqa
        "to_user": lookups["user"].get(wfi.to_user_id),  # noqa
        "draft_status_before": wfi.draft_status_before,
        "draft_status_after": wfi.draft_status_after,
        "timestamp": wfi.timestamp,
        "comment": wfi.comment or "",
        "resolved": wfi.resolved,
        "replies": cast(list[WFReplyDict], wfi.replies) or [],
        "__typename": "DealWorkflowInfo" if is_deal else "InvestorWorkflowInfo",
    }


def base_obj_to_dict(
    obj: Deal | Investor,
    lookups: Lookups,
) -> DealDict | InvestorDict:
    last_version = obj.versions.order_by("created_at").last()

    base_obj_dict: BaseObjDict = {
        "id": obj.id,
        "country": lookups["country"].get(obj.country_id),  # noqa
        "status": obj.status,
        "draft_status": obj.draft_status,
        "created_at": obj.created_at,
        "created_by": lookups["user"].get(obj.created_by_id),  # noqa
        "modified_at": (
            last_version.modified_at
            if last_version.modified_at
            else last_version.created_at
        ),
        "modified_by": lookups["user"].get(
            last_version.modified_by_id
            if last_version.modified_by_id
            else last_version.created_by_id
        ),
        "workflowinfos": [
            workflowinfo_to_dict(wfi, lookups) for wfi in obj.workflowinfos.all()
        ],
    }

    return cast(DealDict | InvestorDict, base_obj_dict)


def deal_to_dict(
    deal: Deal,
    lookups: Lookups,
) -> DealDict:
    deal_dict: DealDict = base_obj_to_dict(deal, lookups)
    deal_dict["deal_size"] = int(deal.deal_size)
    deal_dict["fully_updated_at"] = deal.fully_updated_at
    return deal_dict


def investor_to_dict(
    investor: Investor,
    lookups: Lookups,
) -> InvestorDict:
    investor_dict: InvestorDict = base_obj_to_dict(investor, lookups)
    investor_dict["name"] = investor.name
    investor_dict["deals"] = list(investor.deals.order_by("created_at").values("id"))
    return investor_dict
