import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { components } from "$lib/openAPI"
import {
  AgricultureIoI,
  ForestryIoI,
  ImplementationStatus,
  IoIGroup,
  NatureOfDeal,
  NegotiationStatusGroup,
  OtherIoI,
  RenewableEnergyIoI,
  type AreaType,
  type IntentionOfInvestment,
} from "$lib/types/deal"

type ImplementationStatusMap = { [key in ImplementationStatus]: string }
export const implementationStatusMap = derived(
  _,
  ($_): ImplementationStatusMap => ({
    [ImplementationStatus.PROJECT_NOT_STARTED]: $_("Project not started"),
    [ImplementationStatus.STARTUP_PHASE]: $_("Startup phase (no production)"),
    [ImplementationStatus.IN_OPERATION]: $_("In operation (production)"),
    [ImplementationStatus.PROJECT_ABANDONED]: $_("Project abandoned"),
  }),
)

type NegotiationStatusGroupMap = { [key in NegotiationStatusGroup]: string }
export const negotiationStatusGroupMap = derived(
  _,
  ($_): NegotiationStatusGroupMap => ({
    [NegotiationStatusGroup.INTENDED]: $_("Intended"),
    [NegotiationStatusGroup.CONCLUDED]: $_("Concluded"),
    [NegotiationStatusGroup.FAILED]: $_("Failed"),
    [NegotiationStatusGroup.CONTRACT_EXPIRED]: $_("Contract expired"),
  }),
)

type IntentionOfInvestmentGroupMap = { [key in IoIGroup]: string }
export const intentionOfInvestmentGroupMap = derived(
  _,
  ($_): IntentionOfInvestmentGroupMap => ({
    [IoIGroup.AGRICULTURE]: $_("Agriculture"),
    [IoIGroup.FORESTRY]: $_("Forestry"),
    [IoIGroup.RENEWABLE_ENERGY]: $_("Renewable energy"),
    [IoIGroup.OTHER]: $_("Other"),
  }),
)

type IntentionOfInvestmentMap = { [key in IntentionOfInvestment]: string }
export const intentionOfInvestmentMap = derived(
  _,
  ($_): IntentionOfInvestmentMap => ({
    // agriculture
    [AgricultureIoI.BIOFUELS]: $_("Biomass for biofuels"),
    [AgricultureIoI.BIOMASS_ENERGY_GENERATION]: $_(
      "Biomass for energy generation (agriculture)",
    ),
    [AgricultureIoI.FODDER]: $_("Fodder"),
    [AgricultureIoI.FOOD_CROPS]: $_("Food crops"),
    [AgricultureIoI.LIVESTOCK]: $_("Livestock"),
    [AgricultureIoI.NON_FOOD_AGRICULTURE]: $_("Non-food agricultural commodities"),
    [AgricultureIoI.AGRICULTURE_UNSPECIFIED]: $_("Agriculture unspecified"),
    // forestry
    [ForestryIoI.BIOMASS_ENERGY_PRODUCTION]: $_(
      "Biomass for energy generation (forestry)",
    ),
    [ForestryIoI.CARBON]: $_("For carbon sequestration/REDD"),
    [ForestryIoI.FOREST_LOGGING]: $_("Forest logging for wood and fiber"),
    [ForestryIoI.TIMBER_PLANTATION]: $_("Timber plantation for wood and fiber"),
    [ForestryIoI.FORESTRY_UNSPECIFIED]: $_("Forestry unspecified"),
    // renewable energy
    [RenewableEnergyIoI.SOLAR_PARK]: $_("Solar park"),
    [RenewableEnergyIoI.WIND_FARM]: $_("Wind farm"),
    [RenewableEnergyIoI.RENEWABLE_ENERGY]: $_("Renewable energy unspecified"),
    // other
    [OtherIoI.CONVERSATION]: $_("Conservation"),
    [OtherIoI.INDUSTRY]: $_("Industry"),
    [OtherIoI.LAND_SPECULATION]: $_("Land speculation"),
    [OtherIoI.MINING]: $_("Mining"),
    [OtherIoI.OIL_GAS_EXTRACTION]: $_("Oil / Gas extraction"),
    [OtherIoI.TOURISM]: $_("Tourism"),
    [OtherIoI.OTHER]: $_("Other"),
  }),
)

type AreaTypeMap = { [key in AreaType]: string }
export const areaTypeMap = derived(
  _,
  ($_): AreaTypeMap => ({
    production_area: $_("Production area"),
    contract_area: $_("Contract area"),
    intended_area: $_("Intended area"),
  }),
)

type NatureOfDealMap = { [key in NatureOfDeal]: string }
export const natureOfDealMap = derived(
  _,
  ($_): NatureOfDealMap => ({
    [NatureOfDeal.OUTRIGHT_PURCHASE]: $_("Outright purchase"),
    [NatureOfDeal.LEASE]: $_("Lease"),
    [NatureOfDeal.CONCESSION]: $_("Concession"),
    [NatureOfDeal.EXPLOITATION_PERMIT]: $_(
      "Exploitation permit / license / concession (for mineral resources)",
    ),
    [NatureOfDeal.PURE_CONTRACT_FARMING]: $_("Pure contract farming"),
    [NatureOfDeal.OTHER]: $_("Other"),
  }),
)

type ClassificationMap = {
  [key in components["schemas"]["ClassificationEnum"]]: string
}
export const classificationMap = derived(
  _,
  ($_): ClassificationMap => ({
    GOVERNMENT: $_("Government"),
    GOVERNMENT_INSTITUTION: $_("Government institution"),
    STATE_OWNED_COMPANY: $_("State-/government (owned) company"),
    SEMI_STATE_OWNED_COMPANY: $_("Semi state-owned company"),
    ASSET_MANAGEMENT_FIRM: $_("Asset management firm"),
    BILATERAL_DEVELOPMENT_BANK: $_(
      "Bilateral Development Bank / Development Finance Institution",
    ),
    STOCK_EXCHANGE_LISTED_COMPANY: $_("Stock-exchange listed company"),
    COMMERCIAL_BANK: $_("Commercial Bank"),
    INSURANCE_FIRM: $_("Insurance firm"),
    INVESTMENT_BANK: $_("Investment Bank"),
    INVESTMENT_FUND: $_("Investment fund"),
    MULTILATERAL_DEVELOPMENT_BANK: $_("Multilateral Development Bank (MDB)"),
    PRIVATE_COMPANY: $_("Private company"),
    PRIVATE_EQUITY_FIRM: $_("Private equity firm"),
    INDIVIDUAL_ENTREPRENEUR: $_("Individual entrepreneur"),
    NON_PROFIT: $_("Non - Profit organization (e.g. Church, University etc.)"),
    OTHER: $_("Other"),
  }),
)
