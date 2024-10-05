from django.db import models
from django.db.models.aggregates import Count

from apps.landmatrix.models.country import Region
from apps.landmatrix.quality_indicators.dataclass import QualityIndicator


class QISnapshot(models.Model):
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    data = models.JSONField(blank=True, default=dict)

    class Meta:
        abstract = True


class DealQISnapshot(QISnapshot):
    region = models.ForeignKey(
        "Region",
        null=True,
        on_delete=models.PROTECT,
    )
    subset_key = models.CharField(null=True)

    def __str__(self):
        return f"{self.created_at} - {self.region or 'Global'} - {self.subset_key or 'All'}"


class InvestorQISnapshot(QISnapshot):

    def __str__(self):
        return f"{self.created_at}"


def create_deal_qi_counts(region: Region | None, subset_key: str | None):
    from .deal import DealVersion, DealHull
    from apps.landmatrix.quality_indicators.deal import (
        annotate_counts,
        DEAL_QIS,
        DEAL_SUBSETS,
    )

    ids = DealHull.objects.public().values_list("active_version__id", flat=True)
    qs = DealVersion.objects.filter(id__in=ids)

    if region is not None:
        qs = qs.filter(deal__country__region=region)

    subset_lookup = {qi.key: qi for qi in DEAL_SUBSETS}
    if subset := subset_lookup.get(subset_key):
        qs = qs.filter(subset.query())

    return qs.annotate(counts=annotate_counts()).aggregate(**create_counts(DEAL_QIS))


def create_investor_qi_counts():
    from .investor import InvestorVersion, InvestorHull
    from apps.landmatrix.quality_indicators import INVESTOR_QIS

    ids = InvestorHull.objects.normal().values_list("active_version__id", flat=True)
    qs = InvestorVersion.objects.filter(id__in=ids)

    return qs.aggregate(**create_counts(INVESTOR_QIS))


def create_counts(qis: list[QualityIndicator]) -> dict[str, Count]:
    return dict(
        TOTAL=Count("pk", distinct=True),
        **{
            qi.key: Count(
                "pk",
                filter=qi.query(),
                distinct=True,
            )
            for qi in qis
        },
    )


## Alternative approach to defining QI models with fieldnames
#
# from apps.landmatrix.quality_indicators import DEAL_QIS, INVESTOR_QIS
#
# def create_qi_meta(qis: list[QualityIndicator]) -> models.base.ModelBase:
#     class Meta(models.base.ModelBase):
#         def __new__(cls, name, bases, attrs):
#             for item in qis:
#                 field_name = item.key
#                 attrs[field_name] = models.IntegerField(
#                     item.description,
#                     blank=True,
#                     null=True,
#                 )
#
#             return super().__new__(cls, name, bases, attrs)
#
#     return Meta
#
#
# class DealQI(models.Model, metaclass=create_qi_meta(DEAL_QIS)):
#     pass
#
# class InvestorQI(models.Model, metaclass=create_qi_meta(INVESTOR_QIS)):
#     pass
