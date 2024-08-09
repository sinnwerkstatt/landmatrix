from django.db import models


class DealTopInvestors(models.Model):
    """A view on dealversion.top_investors M2M relation table."""

    dealversion = models.ForeignKey(
        "DealVersion",
        on_delete=models.CASCADE,
        related_name="+",
    )
    investorhull = models.ForeignKey(
        "InvestorHull",
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "landmatrix_dealversion_top_investors"

    def __str__(self):
        return f"#{self.dealversion.deal_id} - {self.investorhull.active_version.name}"
