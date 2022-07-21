export const implementation_status_choices: { [key: string]: string } = {
  PROJECT_NOT_STARTED: "Project not started",
  STARTUP_PHASE: "Start-up phase (no production)",
  IN_OPERATION: "In operation (production)",
  PROJECT_ABANDONED: "Project abandoned",
};

export const nature_of_deal_choices = {
  OUTRIGHT_PURCHASE: "Outright purchase",
  LEASE: "Lease",
  CONCESSION: "Concession",
  EXPLOITATION_PERMIT:
    "Exploitation permit / license / concession (for mineral resources)",
  PURE_CONTRACT_FARMING: "Pure contract farming",
  OTHER: "Other",
};

export const negotiation_status_choices: {
  [key: string]: { [key: string]: string } | string;
} = {
  Intended: {
    EXPRESSION_OF_INTEREST: "Expression of interest",
    UNDER_NEGOTIATION: "Under negotiation",
    MEMORANDUM_OF_UNDERSTANDING: "Memorandum of understanding",
  },
  Concluded: {
    ORAL_AGREEMENT: "Oral agreement",
    CONTRACT_SIGNED: "Contract signed",
    CHANGE_OF_OWNERSHIP: "Change of ownership",
  },
  Failed: {
    NEGOTIATIONS_FAILED: "Negotiations failed",
    CONTRACT_CANCELED: "Contract canceled",
  },

  CONTRACT_EXPIRED: "Contract expired",
};

export const flat_negotiation_status_map: {
  [key: string]: string;
} = {
  EXPRESSION_OF_INTEREST: "Expression of interest",
  UNDER_NEGOTIATION: "Under negotiation",
  MEMORANDUM_OF_UNDERSTANDING: "Memorandum of understanding",
  INTENDED: "Intended",
  ORAL_AGREEMENT: "Oral agreement",
  CONTRACT_SIGNED: "Contract signed",
  CONCLUDED: "Concluded",
  CHANGE_OF_OWNERSHIP: "Change of ownership",
  NEGOTIATIONS_FAILED: "Negotiations failed",
  CONTRACT_CANCELED: "Contract canceled",
  FAILED: "Failed",
  CONTRACT_EXPIRED: "Contract expired",
};

export const intention_of_investment_choices = {
  Agriculture: {
    BIOFUELS: "Biofuels",
    FOOD_CROPS: "Food crops",
    FODDER: "Fodder",
    LIVESTOCK: "Livestock",
    NON_FOOD_AGRICULTURE: "Non-food agricultural commodities",
    AGRICULTURE_UNSPECIFIED: "Agriculture unspecified",
  },
  Forestry: {
    TIMBER_PLANTATION: "Timber plantation",
    FOREST_LOGGING: "Forest logging / management",
    CARBON: "For carbon sequestration/REDD",
    FORESTRY_UNSPECIFIED: "Forestry unspecified",
  },

  Other: {
    MINING: "Mining",
    OIL_GAS_EXTRACTION: "Oil / Gas extraction",
    TOURISM: "Tourism",
    INDUSTRY: "Industry",
    CONVERSATION: "Conservation",
    LAND_SPECULATION: "Land speculation",
    RENEWABLE_ENERGY: "Renewable energy",
    OTHER: "Other",
  },
};

export const flat_intention_of_investment_map = {
  BIOFUELS: "Biofuels",
  FOOD_CROPS: "Food crops",
  FODDER: "Fodder",
  LIVESTOCK: "Livestock",
  NON_FOOD_AGRICULTURE: "Non-food agricultural commodities",
  AGRICULTURE_UNSPECIFIED: "Agriculture unspecified",

  TIMBER_PLANTATION: "Timber plantation",
  FOREST_LOGGING: "Forest logging / management",
  CARBON: "For carbon sequestration/REDD",
  FORESTRY_UNSPECIFIED: "Forestry unspecified",

  MINING: "Mining",
  OIL_GAS_EXTRACTION: "Oil / Gas extraction",
  TOURISM: "Tourism",
  INDUSTRY: "Industry",
  CONVERSATION: "Conservation",
  LAND_SPECULATION: "Land speculation",
  RENEWABLE_ENERGY: "Renewable energy",
  OTHER: "Other",
};

export const classification_choices: { [key: string]: string } = {
  GOVERNMENT: "Government",
  GOVERNMENT_INSTITUTION: "Government institution",
  STATE_OWNED_COMPANY: "State-/government (owned) company",
  SEMI_STATE_OWNED_COMPANY: "Semi state-owned company",
  ASSET_MANAGEMENT_FIRM: "Asset management firm",
  BILATERAL_DEVELOPMENT_BANK:
    "Bilateral Development Bank / Development Finance Institution",
  STOCK_EXCHANGE_LISTED_COMPANY: "Stock-exchange listed company",
  COMMERCIAL_BANK: "Commercial Bank",
  INSURANCE_FIRM: "Insurance firm",
  INVESTMENT_BANK: "Investment Bank",
  INVESTMENT_FUND: "Investment fund",
  MULTILATERAL_DEVELOPMENT_BANK: "Multilateral Development Bank (MDB)",
  PRIVATE_COMPANY: "Private company",
  PRIVATE_EQUITY_FIRM: "Private equity firm",
  INDIVIDUAL_ENTREPRENEUR: "Individual entrepreneur",
  NON_PROFIT: "Non - Profit organization (e.g. Church, University etc.)",
  OTHER: "Other (please specify in comment field)",
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
