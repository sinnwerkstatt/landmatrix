from collections.abc import Callable, Iterable
from datetime import datetime
from typing import TypedDict, TypeVar, cast, overload

from django.db.models import Model

from apps.landmatrix.models.new import InvestorHull, DealHull


class WFReplyDict(TypedDict):
    timestamp: str
    user_id: int
    comment: str


class WorkflowInfoDict(TypedDict):
    id: int
    comment: str
    from_user_id: int
    to_user_id: int | None
    status_before: str | None
    status_after: str | None
    timestamp: datetime
    resolved: bool
    replies: list[WFReplyDict]


class BaseObjDict(TypedDict):
    id: int
    country_id: int | None
    # status: int
    # draft_status: int
    created_at: datetime
    created_by_id: int | None
    modified_at: datetime | None
    modified_by_id: int | None
    workflowinfos: list[WorkflowInfoDict]


class DealDict(BaseObjDict):
    deal_size: int
    fully_updated_at: datetime | None


class InvestorDict(BaseObjDict):
    name: str
    deals: list[int]


T = TypeVar("T", bound=Model)
V = TypeVar("V")


def create_model_lookup(
    qs: Iterable[T],
    map_fn: Callable[[T], V],
) -> dict[int, V]:
    return {val.pk: map_fn(val) for val in qs}


@overload
def base_obj_to_dict(obj: DealHull) -> DealDict:
    ...


@overload
def base_obj_to_dict(obj: InvestorHull) -> InvestorDict:
    ...


def base_obj_to_dict(
    obj: DealHull | InvestorHull,
) -> DealDict | InvestorDict:
    selected_version = obj.active_version or obj.draft_version
    base_obj_dict: BaseObjDict = {
        "id": obj.id,
        "country_id": obj.country_id,
        # "status": obj.status,
        # "draft_status": obj.draft_status,
        "created_at": obj.first_created_at,
        "created_by_id": obj.first_created_by_id,
        "modified_at": selected_version.created_at,
        "modified_by_id": selected_version.created_by_id,
        # "workflowinfos": list(
        #     obj.workflowinfos.all().values(
        #         "id",
        #         "from_user_id",
        #         "to_user_id",
        #         "status_before",
        #         "status_after",
        #         "timestamp",
        #         "comment",
        #         "resolved",
        #         "replies",
        #     )
        # ),
        "workflowinfos": [],
    }

    return cast(DealDict | InvestorDict, base_obj_dict)


def deal_to_dict(deal: DealHull) -> DealDict:
    selected_version = deal.active_version or deal.draft_version

    deal_dict = base_obj_to_dict(deal)
    deal_dict.update(
        {
            "deal_size": int(selected_version.deal_size),
            "fully_updated_at": deal.fully_updated_at,
        }
    )
    return deal_dict


def investor_to_dict(
    investor: InvestorHull,
) -> InvestorDict:
    investor_dict = base_obj_to_dict(investor)
    # investor_dict["name"] = investor.name
    # investor_dict["deals"] = list(investor.deals.order_by("created_at").values("id"))
    return investor_dict
