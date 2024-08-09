from django.db import models

from apps.landmatrix.models.abstract.workflowinfo import _WorkflowInfo


class InvestorWorkflowInfo(_WorkflowInfo):
    investor = models.ForeignKey(
        "InvestorHull",
        on_delete=models.CASCADE,
        related_name="workflowinfos",
    )
    investor_version = models.ForeignKey(
        "InvestorVersion",
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "investor_id": self.investor_id,
                "investor_version_id": self.investor_version_id,
            }
        )
        return d

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/investor/{self.investor_id}/"
