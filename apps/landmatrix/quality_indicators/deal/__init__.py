from django.utils.translation import gettext_lazy as _

from .subsets import *
from ..dataclass import QualityIndicator, Subset
from .queries import *
from apps.landmatrix.models.choices import IntentionOfInvestmentGroupEnum

DEAL_QIS: list[QualityIndicator] = [
    QualityIndicator(
        key="locations/any-georeferenced-or-high-accuracy",
        name=_("At least one location georeferenced with high accuracy."),
        description=_(
            "Deals for which at least one deal location is georeferenced "
            "with high accuracy: Accuracy level = 'exact location' "
            "OR accuracy level = 'coordinates' "
            "OR georeferenced area data given / polygon given."
        ),
        query=lambda: q_any_location_georeferenced_or_high_accuracy(),
    ),
    QualityIndicator(
        key="locations/all-georeferenced-or-high-accuracy",
        name=_("All locations georeferenced with high accuracy."),
        description=_(
            "Deals for which all deal location is georeferenced "
            "with high accuracy: Accuracy level = 'exact location' "
            "OR accuracy level = 'coordinates' "
            "OR georeferenced area data given / polygon given."
        ),
        query=lambda: q_all_location_georeferenced_or_high_accuracy(),
    ),
    # QualityIndicator(
    #     key="locations/all-high-accuracy-and-marker-or-polygon-data-given",
    #     name=_("Location markers in polygon region"),
    #     description=_(
    #         "Deals with all locations having a high spatial accuracy level "
    #         "(exact or coordinates) and a point location chosen and/or a polygon given"
    #     ),
    #     query=lambda: Q(),
    # ),
    # QualityIndicator(
    #     key="locations/all-markers-in-polygon-region",
    #     name=_("Location markers in polygon region"),
    #     description=_(
    #         "Deals with polygon data given and for each location polygon "
    #         "showing respective coordinates located within that polygons."
    #     ),
    #     query=lambda: Q(),
    # ),
    QualityIndicator(
        key="locations/any-georeferenced",
        name=_("Spatially localised by at least one georeferenced polygon."),
        description=_(
            "Deals for which georeferenced area data (polygon) is given "
            "for the intended area and/or for the area under contract "
            "and/or for the area in operation of at least one deal location."
        ),
        query=lambda: q_any_location_georeferenced(),
    ),
    QualityIndicator(
        key="locations/all-georeferenced",
        name=_("Spatially localised by georeferenced polygons for all deal locations."),
        description=_(
            "Deals for which georeferenced area data (polygon) is given "
            "for the intended area and/or for the area under contract "
            "and/or for the area in operation of all deal locations."
        ),
        query=lambda: q_all_location_georeferenced(),
    ),
    QualityIndicator(
        key="locations/any-georeferenced-as-contract",
        name=_(
            "Spatially localised by a georeferenced polygon for the area under contract."
        ),
        description=_(
            "Deals for which georeferenced area data (polygon) is given "
            "for the area under contract of at least one deal location."
        ),
        query=lambda: q_any_location_georeferenced_as_contract(),
    ),
    QualityIndicator(
        key="locations/any-georeferenced-as-production",
        name=_(
            "Spatially localised by a georeferenced polygon for the area in operation."
        ),
        description=_(
            "Deals for which georeferenced area data (polygon) is given "
            "for the area in operation of at least one deal location."
        ),
        query=lambda: q_any_location_georeferenced_as_production(),
    ),
    QualityIndicator(
        key="data-sources/has-multiple",
        name=_("Deals with multiple data sources."),
        description=_(
            "Deals for which more than one data source of any type is given."
        ),
        query=lambda: q_multiple_datasource(),
    ),
    QualityIndicator(
        key="data-sources/all-valid",
        name=_("Data source files given."),
        description=_(
            "Deals for which all data source files are given for data sources of "
            "type = contract, "
            "type = contract (contract farming agreement), "
            "type = research paper / policy report, "
            "type = company sources, "
            "type = government sources and "
            "type = media report."
        ),
        query=lambda: q_all_datasource_valid(),
    ),
    QualityIndicator(
        key="imp-and-neg-status",
        name=_("Negotiation and implementation status given."),
        description=_(
            "Deals for which a negotiation status and an implementation status are given."
        ),
        query=lambda: q_all_status(),
    ),
    QualityIndicator(
        key="imp-and-neg-status-dated",
        name=_("Negotiation and implementation status given with date."),
        description=_(
            "Deals for which the year or date is given for the negotiation status "
            "and the implementation status."
        ),
        query=lambda: q_all_status_dated(),
    ),
    QualityIndicator(
        key="imp-and-neg-status-and-area-dated",
        name=_(
            "Negotiation status, implementation status and area size given with date."
        ),
        description=_(
            "Deals for which the year or date is given for at least one area size "
            "(size of intended area and/or area under contract and/or area in operation), "
            "for negotiation status and for implementation status."
        ),
        query=lambda: q_all_status_dated_and_any_area_dated(),
    ),
    QualityIndicator(
        key="production-or-contract-area-dated",
        name=_("Size under contract or size in operation given with date."),
        description=_(
            "Deals for which the year or date is given for the "
            "area size under contract or for the area size in operation."
        ),
        query=lambda: q_any_area_dated(),
    ),
    QualityIndicator(
        key="all-basic-fields",
        name=_("Data given for multiple key variables."),
        description=_(
            "Deals for which the area size under contract, "
            "the intention of investment, the negotiation status, "
            "the implementation status, the nature of the deal and "
            "the produce info ("
            "Choice of Crops "
            "OR Choice of Livestock "
            "OR Choice of Mineral resources "
            "OR Choice of Contract farming crop "
            "OR Contract farming livestock "
            "OR Choice of Electricity generation "
            "OR Choice of Carbon sequestration/offsetting given"
            ")."
        ),
        query=lambda: q_all_basic_fields(),
    ),
    QualityIndicator(
        key="any-produce-info",
        name=_("Produce info given."),
        description=_(
            "Deals with produce info given ("
            "Choice of Crops "
            "OR Choice of Livestock "
            "OR Choice of Mineral resources "
            "OR Choice of Contract farming crop "
            "OR Contract farming livestock "
            "OR Choice of Electricity generation "
            "OR Choice of Carbon sequestration/offsetting given"
            ")."
        ),
        query=lambda: q_any_produce_info(),
    ),
    QualityIndicator(
        key="operating-company-in-target-country",
        name=_(
            "Operating company's country of origin corresponds to the target country of the deal."
        ),
        description=_(
            "Deals involving an operating company that originates from a country "
            "that corresponds to the target country of the deal."
        ),
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
