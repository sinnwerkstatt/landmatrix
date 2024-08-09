from django.db import models

from apps.landmatrix.models.abstract.datasource import BaseDataSource


class InvestorDataSource(BaseDataSource):
    investorversion = models.ForeignKey(
        "InvestorVersion",
        on_delete=models.CASCADE,
        related_name="datasources",
    )

    class Meta:
        unique_together = ["investorversion", "nid"]
        indexes = [models.Index(fields=["investorversion", "nid"])]
        ordering = ["id"]
