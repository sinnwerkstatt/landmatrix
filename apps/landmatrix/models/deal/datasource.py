from django.db import models

from apps.landmatrix.models.abstract.datasource import BaseDataSource


class DealDataSource(BaseDataSource):
    dealversion = models.ForeignKey(
        "DealVersion",
        on_delete=models.CASCADE,
        related_name="datasources",
    )

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]
