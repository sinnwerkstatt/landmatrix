import {
  ImplementationStatus,
  IntentionOfInvestment,
  IntentionOfInvestmentGroup,
  NatureOfDeal,
  NegotiationStatus,
  NegotiationStatusGroup,
} from "$lib/types/deal";
import { Classification } from "$lib/types/investor";

export const implementation_status_choices: { [key in ImplementationStatus]: string } =
  {
    [ImplementationStatus.PROJECT_NOT_STARTED]: "Project not started",
    [ImplementationStatus.STARTUP_PHASE]: "Startup phase (no production)",
    [ImplementationStatus.IN_OPERATION]: "In operation (production)",
    [ImplementationStatus.PROJECT_ABANDONED]: "Project abandoned",
  };

export const nature_of_deal_choices: { [key in NatureOfDeal]: string } = {
  [NatureOfDeal.OUTRIGHT_PURCHASE]: "Outright purchase",
  [NatureOfDeal.LEASE]: "Lease",
  [NatureOfDeal.CONCESSION]: "Concession",
  [NatureOfDeal.EXPLOITATION_PERMIT]:
    "Exploitation permit / license / concession (for mineral resources)",
  [NatureOfDeal.PURE_CONTRACT_FARMING]: "Pure contract farming",
  [NatureOfDeal.OTHER]: "Other",
};

export const flat_negotiation_status_map: {
  [key in NegotiationStatus | NegotiationStatusGroup]: string;
} = {
  [NegotiationStatus.EXPRESSION_OF_INTEREST]: "Expression of interest",
  [NegotiationStatus.UNDER_NEGOTIATION]: "Under negotiation",
  [NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING]: "Memorandum of understanding",
  [NegotiationStatus.ORAL_AGREEMENT]: "Oral agreement",
  [NegotiationStatus.CONTRACT_SIGNED]: "Contract signed",
  [NegotiationStatus.CHANGE_OF_OWNERSHIP]: "Change of ownership",
  [NegotiationStatus.NEGOTIATIONS_FAILED]: "Negotiations failed",
  [NegotiationStatus.CONTRACT_CANCELED]: "Contract canceled",

  [NegotiationStatusGroup.INTENDED]: "Intended",
  [NegotiationStatusGroup.CONCLUDED]: "Concluded",
  [NegotiationStatusGroup.FAILED]: "Failed",
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: "Contract expired",
};

export const negotiation_status_group_choices: {
  [key in NegotiationStatusGroup]: string;
} = {
  [NegotiationStatusGroup.INTENDED]: "Intended",
  [NegotiationStatusGroup.CONCLUDED]: "Concluded",
  [NegotiationStatusGroup.FAILED]: "Failed",
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: "Contract expired",
};

export const agriculture_investment_choices = {
  [IntentionOfInvestment.BIOFUELS]: "Biofuels",
  [IntentionOfInvestment.FOOD_CROPS]: "Food crops",
  [IntentionOfInvestment.FODDER]: "Fodder",
  [IntentionOfInvestment.LIVESTOCK]: "Livestock",
  [IntentionOfInvestment.NON_FOOD_AGRICULTURE]: "Non-food agricultural commodities",
  [IntentionOfInvestment.AGRICULTURE_UNSPECIFIED]: "Agriculture unspecified",
};

export const forestry_investment_choices = {
  [IntentionOfInvestment.TIMBER_PLANTATION]: "Timber plantation",
  [IntentionOfInvestment.FOREST_LOGGING]: "Forest logging / management",
  [IntentionOfInvestment.CARBON]: "For carbon sequestration/REDD",
  [IntentionOfInvestment.FORESTRY_UNSPECIFIED]: "Forestry unspecified",
};

export const other_intention_choices = {
  [IntentionOfInvestment.MINING]: "Mining",
  [IntentionOfInvestment.OIL_GAS_EXTRACTION]: "Oil / Gas extraction",
  [IntentionOfInvestment.TOURISM]: "Tourism",
  [IntentionOfInvestment.INDUSTRY]: "Industry",
  [IntentionOfInvestment.CONVERSATION]: "Conservation",
  [IntentionOfInvestment.LAND_SPECULATION]: "Land speculation",
  [IntentionOfInvestment.RENEWABLE_ENERGY]: "Renewable energy",
  [IntentionOfInvestment.OTHER]: "Other",
};

export const intention_of_investment_group_choices: {
  [key in IntentionOfInvestmentGroup]: string;
} = {
  [IntentionOfInvestmentGroup.AGRICULTURE]: "Agriculture",
  [IntentionOfInvestmentGroup.FORESTRY]: "Forestry",
  [IntentionOfInvestmentGroup.OTHER]: "Other",
};

export const intention_of_investment_choices = {
  Agriculture: agriculture_investment_choices,
  Forestry: forestry_investment_choices,
  Other: other_intention_choices,
};

export const flat_intention_of_investment_map: {
  [key in IntentionOfInvestment]: string;
} = {
  ...agriculture_investment_choices,
  ...forestry_investment_choices,
  ...other_intention_choices,
};

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
};

export const status_map = {
  1: "Draft",
  2: "Active", //"Live",
  3: "Active", // "Updated",
  4: "Deleted",
  5: "Rejected", // legacy
  6: "To Delete", // legacy
};
export const draft_status_map = {
  1: "Draft",
  2: "Review",
  3: "Activation",
  4: "Rejected", // legacy
  5: "Deleted",
};

export const combined_status_fn = (
  status: number,
  draft_status: number | null,
  toString = false
): string => {
  if (status === 4) return toString ? "Deleted" : "DELETED";
  if (draft_status === 1) return toString ? "Draft" : "DRAFT";
  if (draft_status === 2) return toString ? "Submitted for review" : "REVIEW";
  if (draft_status === 3) return toString ? "Submitted for activation" : "ACTIVATION";
  if (draft_status === 4) return toString ? "Rejected" : "REJECTED";
  if (draft_status === 5) return toString ? "To Delete" : "TO_DELETE";
  if ([2, 3].includes(status) && draft_status === null)
    return toString ? "Active" : "ACTIVE";
  throw Error(`Invalid status ${status} ${draft_status}`);
};
