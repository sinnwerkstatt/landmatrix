from django.db.models.query_utils import Q

from apps.landmatrix.models.choices import (
    INTENTION_OF_INVESTMENT_ITEMS,
    NEGOTIATION_STATUS_ITEMS,
    IntentionOfInvestmentGroupEnum,
    NegotiationStatusGroupEnum,
)

__all__ = (
    "q_default",
    "q_transnational",
    "q_ioi_group",
    "q_carbon_offsetting",
    "q_carbon_sequestration",
    "q_electricity_generation",
    "q_green_deals",
)


def q_default() -> Q:
    return Q(
        deal_size__gte=200,
        initiation_year__gte=2000,
        transnational=True,
        forest_concession=False,
        current_negotiation_status__in=[
            ioi["value"]
            for ioi in NEGOTIATION_STATUS_ITEMS
            if ioi["group"] == NegotiationStatusGroupEnum.CONCLUDED
        ],
        current_intention_of_investment__overlap=[
            ioi["value"]
            for ioi in INTENTION_OF_INVESTMENT_ITEMS
            if ioi["value"] not in ["MINING", "OIL_GAS_EXTRACTION"]
        ],
    ) & ~Q(nature_of_deal__contained_by=["OTHER", "PURE_CONTRACT_FARMING"])


def q_transnational() -> Q:
    return Q(transnational=True)


def q_ioi_group(group: IntentionOfInvestmentGroupEnum) -> Q:
    return Q(
        current_intention_of_investment__overlap=[
            ioi["value"]
            for ioi in INTENTION_OF_INVESTMENT_ITEMS
            if ioi["group"] == group
        ],
    )


def q_carbon_offsetting() -> Q:
    return Q(carbon_offset_project=True)


def q_carbon_sequestration() -> Q:
    return Q(current_carbon_sequestration__len__gt=0)


def q_electricity_generation() -> Q:
    return Q(current_electricity_generation__len__gt=0)


def q_green_deals() -> Q:
    return (
        q_carbon_offsetting()
        | q_carbon_sequestration()
        | q_electricity_generation()
        | Q(
            current_intention_of_investment__overlap=[
                "BIOFUELS",
                "BIOMASS_ENERGY_GENERATION",
                "BIOMASS_ENERGY_PRODUCTION",
                "CARBON",
                "SOLAR_PARK",
                "WIND_FARM",
            ]
        )
    )
