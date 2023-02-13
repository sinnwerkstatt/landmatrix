from apps.accounts.models import User
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)

from typing import Type
from django.contrib.auth import get_user_model

UserModel: Type[User] = get_user_model()


def user_to_dict(user: User | None):
    if user is None:
        return

    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
    }


def version_to_dict(version: DealVersion | InvestorVersion):
    return {
        "id": version.id,
        "created_at": version.created_at,
        "created_by": user_to_dict(version.created_by),
        "modified_at": version.modified_at,
        "modified_by": user_to_dict(version.modified_by),
    }


def workflowinfo_to_dict(wfi: DealWorkflowInfo | InvestorWorkflowInfo):
    is_deal = isinstance(wfi, DealWorkflowInfo)
    return {
        "id": wfi.id,
        "from_user": user_to_dict(wfi.from_user),
        "to_user": user_to_dict(wfi.to_user),
        "draft_status_before": wfi.draft_status_before,
        "draft_status_after": wfi.draft_status_after,
        "obj_version_id": wfi.deal_version_id if is_deal else wfi.investor_version_id,
        "timestamp": wfi.timestamp,
        "comment": wfi.comment or "",
        "resolved": wfi.resolved,
        "replies": wfi.replies or [],
        "__typename": "DealWorkflowInfo" if is_deal else "InvestorWorkflowInfo",
    }


def deal_to_dict(deal: Deal):
    last_version = deal.versions.order_by("created_at").last()
    return {
        "id": deal.id,
        "country_id": deal.country_id,
        "status": deal.status,
        "draft_status": deal.draft_status,
        "created_at": deal.created_at,
        "created_by": user_to_dict(deal.created_by),
        "last_version": version_to_dict(last_version),
        "workflowinfos": [
            workflowinfo_to_dict(wfi) for wfi in deal.workflowinfos.all()
        ],
    }


def main():
    from timeit import default_timer
    from django.db.models import Prefetch

    qs_all_deals = Deal.objects.prefetch_related(
        Prefetch(
            "versions",
            queryset=DealVersion.objects.defer("serialized_data").order_by(
                "created_at"
            ),
        ),
        Prefetch(
            "workflowinfos",
            queryset=DealWorkflowInfo.objects.order_by("timestamp"),
        ),
    ).all()

    start = default_timer()

    deals = [deal_to_dict(deal) for deal in qs_all_deals]
    end = default_timer()

    print(deals[0])
    print(f"new query duration {end-start:.3f}s")
    print()
    return
