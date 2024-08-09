from django.db import models

from apps.landmatrix.models.abstract.workflowinfo import _WorkflowInfo


class DealWorkflowInfo(_WorkflowInfo):
    deal = models.ForeignKey(
        "DealHull",
        on_delete=models.CASCADE,
        related_name="workflowinfos",
    )
    deal_version = models.ForeignKey(
        "DealVersion",
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    # OLD Code
    # # WARNING
    # # Do not use to map large query sets!
    # # Takes tons of memory storing related deal and deal_version objects.
    # def to_dict(self) -> dict:
    #     d = super().to_dict()
    #     d.update({"deal": self.deal, "deal_version": self.deal_version})
    #     return d

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"deal_id": self.deal_id, "deal_version_id": self.deal_version_id})
        return d

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/deal/{self.deal_id}/"
