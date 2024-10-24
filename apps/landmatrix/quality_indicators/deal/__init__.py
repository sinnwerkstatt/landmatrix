from django.utils.translation import gettext_lazy as _

from .subsets import *
from ..dataclass import QualityIndicator, Subset
from .queries import *
from apps.landmatrix.models.choices import IntentionOfInvestmentGroupEnum

DEAL_QIS: list[QualityIndicator] = [
    QualityIndicator(
        key="locations/any-georeferenced-or-high-accuracy",
        name=_("Any location is georeferenced or marked as high accuracy."),
        description=_(""),
        query=lambda: q_any_location_georeferenced_or_high_accuracy(),
    ),
    QualityIndicator(
        key="locations/all-georeferenced-or-high-accuracy",
        name=_("All locations are georeferenced or marked as high accuracy."),
        description=_(""),
        query=lambda: q_all_location_georeferenced_or_high_accuracy(),
    ),
    QualityIndicator(
        key="locations/any-georeferenced",
        name=_("Any location is georeferenced."),
        description=_(""),
        query=lambda: q_any_location_georeferenced(),
    ),
    QualityIndicator(
        key="locations/all-georeferenced",
        name=_("All locations are georeferenced."),
        description=_(""),
        query=lambda: q_all_location_georeferenced(),
    ),
    QualityIndicator(
        key="locations/any-georeferenced-as-contract",
        name=_("Any location is georeferenced as contract area."),
        description=_(""),
        query=lambda: q_any_location_georeferenced_as_contract(),
    ),
    QualityIndicator(
        key="locations/any-georeferenced-as-production",
        name=_("Any location is georeferenced as production area."),
        description=_(""),
        query=lambda: q_any_location_georeferenced_as_production(),
    ),
    QualityIndicator(
        key="data-sources/has-multiple",
        name=_("Has multiple data sources."),
        description=_(""),
        query=lambda: q_multiple_datasource(),
    ),
    QualityIndicator(
        key="data-sources/all-valid",
        name=_("All data sources that require a file have a file."),
        description=_(""),
        query=lambda: q_all_datasource_valid(),
    ),
    QualityIndicator(
        key="imp-and-neg-status",
        name=_("Negotiation status and implementation status given."),
        description=_(""),
        query=lambda: q_all_status(),
    ),
    QualityIndicator(
        key="imp-and-neg-status-dated",
        name=_("Negotiation status and implementation status given with dates."),
        description=_(""),
        query=lambda: q_all_status_dated(),
    ),
    QualityIndicator(
        key="imp-and-neg-status-and-area-dated",
        name=_("Negotiation status, implementation status and area given with dates."),
        description=_(""),
        query=lambda: q_all_status_dated_and_any_area_dated(),
    ),
    QualityIndicator(
        key="production-or-contract-area-dated",
        name=_("Production size or contract size given with dates."),
        description=_(""),
        query=lambda: q_any_area_dated(),
    ),
    QualityIndicator(
        key="all-basic-fields",
        name=_(
            "Contract size, intention of investment, negotiation status, "
            "implementation status, nature of deal AND any produce info given."
        ),
        description=_(""),
        query=lambda: q_all_basic_fields(),
    ),
    QualityIndicator(
        key="any-produce-info",
        name=_(
            "(Contract farming) crops, (contract farming) animals, minerals, "
            "electricity generation OR carbon sequestration given.",
        ),
        description=_(""),
        query=lambda: q_any_produce_info(),
    ),
    QualityIndicator(
        key="operating-company-in-target-country",
        name=_("Operating company registered in target country"),
        description=_(""),
        query=lambda: q_operating_company_in_target_country(),
    ),
]


DEAL_SUBSETS: list[Subset] = [
    Subset(
        key="DEFAULT_FILTER",
        description=_("Default filter"),
        query=lambda: q_default(),
    ),
    Subset(
        key="AGRICULTURE_TRANSNATIONAL",
        description=_("Agriculture transnational"),
        query=lambda: q_transnational()
        & q_ioi_group(IntentionOfInvestmentGroupEnum.AGRICULTURE),
    ),
    Subset(
        key="FORESTRY_TRANSNATIONAL",
        description=_("Forestry transnational"),
        query=lambda: q_transnational()
        & q_ioi_group(IntentionOfInvestmentGroupEnum.FORESTRY),
    ),
    Subset(
        key="RENEWABLE_ENERGY_POWER_PLANTS",
        description=_("Renewable energy power plants"),
        query=lambda: q_ioi_group(IntentionOfInvestmentGroupEnum.RENEWABLE_ENERGY),
    ),
    Subset(
        key="CARBON_OFFSETTING",
        description=_("Carbon offsetting"),
        query=lambda: q_carbon_offsetting(),
    ),
    Subset(
        key="CARBON_SEQUESTRATION",
        description=_("Carbon sequestration"),
        query=lambda: q_carbon_sequestration(),
    ),
    Subset(
        key="GREEN_DEALS",
        description=_("Green deals"),
        query=lambda: q_green_deals(),
    ),
]


# # alternative approach to defining query set filters, e.g. quality indicators
# class DealQIQuerySet(QuerySet):
#
#     def default(self):
#         return self.filter(q_default())
#
#     def subset(self, key: str):
#         lookup = {qi.key: qi for qi in DEAL_SUBSETS}
#
#         if subset := lookup.get(key):
#             self.filter(subset.query)
#         else:
#             print(f"Unknown subset: {key}")
#
#         return self
#
# from django.db.models import TextChoices
#
# # alternative approach of defining Subsets using TextChoices Enum and query lookup
# class DealSubset(TextChoices):
#     # ALL = "ALL", _("All (no filters)")
#     DEFAULT = "DEFAULT", _("Default filters")
#     AGRICULTURE_TRANSNATIONAL = (
#         "AGRICULTURE_TRANSNATIONAL",
#         _("Agriculture transnational"),
#     )
#
#
# SUBSET_QUERY_LOOKUP: dict[DealSubset, Q] = {
#     # DealSubset.ALL: Q(),
#     DealSubset.DEFAULT: q_default(),
#     DealSubset.AGRICULTURE_TRANSNATIONAL: (
#         q_transnational() & q_ioi_group(IntentionOfInvestmentGroupEnum.AGRICULTURE)
#     ),
# }
