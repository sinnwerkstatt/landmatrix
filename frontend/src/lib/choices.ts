import {
  AgricultureIoI,
  ForestryIoI,
  ImplementationStatus,
  IntentionOfInvestment,
  IntentionOfInvestmentGroup,
  NatureOfDeal,
  NegotiationStatusGroup,
  OtherIoI,
  RenewableEnergyIoI,
} from "$lib/types/deal"
import { Classification } from "$lib/types/investor"

export const getImplementationStatusChoices = (
  $t: (t: string) => string,
): { [key in ImplementationStatus]: string } => {
  return {
    [ImplementationStatus.PROJECT_NOT_STARTED]: $t("Project not started"),
    [ImplementationStatus.STARTUP_PHASE]: $t("Startup phase (no production)"),
    [ImplementationStatus.IN_OPERATION]: $t("In operation (production)"),
    [ImplementationStatus.PROJECT_ABANDONED]: $t("Project abandoned"),
  }
}

export const implementation_status_choices: { [key in ImplementationStatus]: string } =
  {
    [ImplementationStatus.PROJECT_NOT_STARTED]: "Project not started",
    [ImplementationStatus.STARTUP_PHASE]: "Startup phase (no production)",
    [ImplementationStatus.IN_OPERATION]: "In operation (production)",
    [ImplementationStatus.PROJECT_ABANDONED]: "Project abandoned",
  }

export const getNatureOfDealChoices = (
  $t: (t: string) => string,
): { [key in NatureOfDeal]: string } => {
  return {
    [NatureOfDeal.OUTRIGHT_PURCHASE]: $t("Outright purchase"),
    [NatureOfDeal.LEASE]: $t("Lease"),
    [NatureOfDeal.CONCESSION]: $t("Concession"),
    [NatureOfDeal.EXPLOITATION_PERMIT]: $t(
      "Exploitation permit / license / concession (for mineral resources)",
    ),
    [NatureOfDeal.PURE_CONTRACT_FARMING]: $t("Pure contract farming"),
    [NatureOfDeal.OTHER]: $t("Other"),
  }
}

export const negotiation_status_group_choices: {
  [key in NegotiationStatusGroup]: string
} = {
  [NegotiationStatusGroup.INTENDED]: "Intended",
  [NegotiationStatusGroup.CONCLUDED]: "Concluded",
  [NegotiationStatusGroup.FAILED]: "Failed",
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: "Contract expired",
}

export const agriculture_investment_choices: {
  [key in AgricultureIoI]: string
} = {
  [AgricultureIoI.BIOFUELS]: "Biomass for biofuels",
  [AgricultureIoI.BIOMASS_ENERGY_GENERATION]: "Biomass for energy generation",
  [AgricultureIoI.FODDER]: "Fodder",
  [AgricultureIoI.FOOD_CROPS]: "Food crops",
  [AgricultureIoI.LIVESTOCK]: "Livestock",
  [AgricultureIoI.NON_FOOD_AGRICULTURE]: "Non-food agricultural commodities",
  [AgricultureIoI.AGRICULTURE_UNSPECIFIED]: "Agriculture unspecified",
}

export const forestry_investment_choices: {
  [key in ForestryIoI]: string
} = {
  [ForestryIoI.BIOMASS_ENERGY_PRODUCTION]: "Biomass for energy generation",
  [ForestryIoI.CARBON]: "For carbon sequestration/REDD",
  [ForestryIoI.FOREST_LOGGING]: "Forest logging for wood and fiber",
  [ForestryIoI.TIMBER_PLANTATION]: "Timber plantation for wood and fiber",
  [ForestryIoI.FORESTRY_UNSPECIFIED]: "Forestry unspecified",
}
export const renewable_energy_investment_choices: {
  [key in RenewableEnergyIoI]: string
} = {
  [RenewableEnergyIoI.SOLAR_PARK]: "Solar park",
  [RenewableEnergyIoI.WIND_FARM]: "Wind farm",
  [RenewableEnergyIoI.RENEWABLE_ENERGY]: "Renewable energy unspecified",
}
export const other_intention_choices: { [key in OtherIoI]: string } = {
  [OtherIoI.CONVERSATION]: "Conservation",
  [OtherIoI.INDUSTRY]: "Industry",
  [OtherIoI.LAND_SPECULATION]: "Land speculation",
  [OtherIoI.MINING]: "Mining",
  [OtherIoI.OIL_GAS_EXTRACTION]: "Oil / Gas extraction",
  [OtherIoI.TOURISM]: "Tourism",
  [OtherIoI.OTHER]: "Other",
}

export const intention_of_investment_group_choices: {
  [key in IntentionOfInvestmentGroup]: string
} = {
  [IntentionOfInvestmentGroup.AGRICULTURE]: "Agriculture",
  [IntentionOfInvestmentGroup.FORESTRY]: "Forestry",
  [IntentionOfInvestmentGroup.RENEWABLE_ENERGY]: "Renewable energy",
  [IntentionOfInvestmentGroup.OTHER]: "Other",
}

export const intention_of_investment_choices = {
  Agriculture: agriculture_investment_choices,
  Forestry: forestry_investment_choices,
  "Renewable energy power plants": renewable_energy_investment_choices,
  Other: other_intention_choices,
}

export const flat_intention_of_investment_map: {
  [key in IntentionOfInvestment]: string
} = {
  ...agriculture_investment_choices,
  ...forestry_investment_choices,
  ...renewable_energy_investment_choices,
  ...other_intention_choices,
}

export const classification_choices: { [key in Classification]: string } = {
  [Classification.GOVERNMENT]: "Government",
  [Classification.GOVERNMENT_INSTITUTION]: "Government institution",
  [Classification.STATE_OWNED_COMPANY]: "State-/government (owned) company",
  [Classification.SEMI_STATE_OWNED_COMPANY]: "Semi state-owned company",
  [Classification.ASSET_MANAGEMENT_FIRM]: "Asset management firm",
  [Classification.BILATERAL_DEVELOPMENT_BANK]:
    "Bilateral Development Bank / Development Finance Institution",
  [Classification.STOCK_EXCHANGE_LISTED_COMPANY]: "Stock-exchange listed company",
  [Classification.COMMERCIAL_BANK]: "Commercial Bank",
  [Classification.INSURANCE_FIRM]: "Insurance firm",
  [Classification.INVESTMENT_BANK]: "Investment Bank",
  [Classification.INVESTMENT_FUND]: "Investment fund",
  [Classification.MULTILATERAL_DEVELOPMENT_BANK]: "Multilateral Development Bank (MDB)",
  [Classification.PRIVATE_COMPANY]: "Private company",
  [Classification.PRIVATE_EQUITY_FIRM]: "Private equity firm",
  [Classification.INDIVIDUAL_ENTREPRENEUR]: "Individual entrepreneur",
  [Classification.NON_PROFIT]:
    "Non - Profit organization (e.g. Church, University etc.)",
  [Classification.OTHER]: "Other (please specify in comment field)",
}
