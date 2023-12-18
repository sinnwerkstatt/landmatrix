from django.core.management.base import BaseCommand

from apps.landmatrix.models.deal import DealWorkflowInfo
from apps.landmatrix.models.investor import InvestorWorkflowInfo
from apps.landmatrix.models.new import DealWorkflowInfo2, InvestorWorkflowInfo2

status_map_dings = {
    1: "DRAFT",
    2: "REVIEW",
    3: "ACTIVATION",
    4: "REJECTED",
    5: "TO_DELETE",
    None: None,
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for wfi_old in DealWorkflowInfo.objects.all():
            wfi_old: DealWorkflowInfo

            status_before = status_map_dings[wfi_old.draft_status_before]
            status_after = status_map_dings[wfi_old.draft_status_after]
            if status_before == "ACTIVATION" and status_after is None:
                status_after = "ACTIVATED"

            DealWorkflowInfo2.objects.create(
                from_user_id=wfi_old.from_user_id,
                to_user_id=wfi_old.to_user_id,
                status_before=status_before,
                status_after=status_after,
                timestamp=wfi_old.timestamp,
                comment=wfi_old.comment or "",
                replies=wfi_old.replies or [],
                resolved=wfi_old.resolved,
                deal_id=wfi_old.deal_id,
                deal_version_id=wfi_old.deal_version_id,
            )

        for wfi_old in InvestorWorkflowInfo.objects.all():
            wfi_old: InvestorWorkflowInfo

            status_before = status_map_dings[wfi_old.draft_status_before]
            status_after = status_map_dings[wfi_old.draft_status_after]
            if status_before == "ACTIVATION" and status_after is None:
                status_after = "ACTIVATED"

            InvestorWorkflowInfo2.objects.create(
                from_user_id=wfi_old.from_user_id,
                to_user_id=wfi_old.to_user_id,
                status_before=status_before,
                status_after=status_after,
                timestamp=wfi_old.timestamp,
                comment=wfi_old.comment or "",
                replies=wfi_old.replies or [],
                resolved=wfi_old.resolved,
                investor_id=wfi_old.investor_id,
                investor_version_id=wfi_old.investor_version_id,
            )
