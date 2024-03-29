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
  },
  Failed: {
    NEGOTIATIONS_FAILED: "Negotiations failed",
    CONTRACT_CANCELED: "Contract canceled",
  },

  CONTRACT_EXPIRED: "Contract expired",
  CHANGE_OF_OWNERSHIP: "Change of ownership",
};
export const negotiation_status_group_map: {
  [key: string]: string | null;
} = {
  EXPRESSION_OF_INTEREST: "INTENDED",
  UNDER_NEGOTIATION: "INTENDED",
  MEMORANDUM_OF_UNDERSTANDING: "INTENDED",
  ORAL_AGREEMENT: "CONCLUDED",
  CONTRACT_SIGNED: "CONCLUDED",
  NEGOTIATIONS_FAILED: "FAILED",
  CONTRACT_CANCELED: "FAILED",
  CONTRACT_EXPIRED: null,
  CHANGE_OF_OWNERSHIP: null,
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
  NEGOTIATIONS_FAILED: "Negotiations failed",
  CONTRACT_CANCELED: "Contract canceled",
  FAILED: "Failed",
  CONTRACT_EXPIRED: "Contract expired",
  CHANGE_OF_OWNERSHIP: "Change of ownership",
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

export const intention_of_investment_map: { [key: string]: string[] } = {
  BIOFUELS: ["Biofuels", "fas fa-leaf"],
  FOOD_CROPS: ["Food crops", "fas fa-carrot"],
  FODDER: ["Fodder", "fas fa-leaf"],
  LIVESTOCK: ["Livestock", "fas fa-paw"],
  NON_FOOD_AGRICULTURE: ["Non-food agricultural commodities", "fas fa-leaf"],
  AGRICULTURE_UNSPECIFIED: ["Agriculture unspecified", "fas fa-leaf"],

  TIMBER_PLANTATION: ["Timber plantation", "fas fa-tree"],
  FOREST_LOGGING: ["Forest logging / management", "fas fa-tree"],
  CARBON: ["For carbon sequestration/REDD", "fas fa-tree"],
  FORESTRY_UNSPECIFIED: ["Forestry unspecified", "fas fa-tree"],

  MINING: ["Mining", "fas fa-mountain"],
  OIL_GAS_EXTRACTION: ["Oil / Gas extraction", "fas fa-oil-can"],
  TOURISM: ["Tourism", "fas fa-plane"],
  INDUSTRY: ["Industry", "fas fa-industry"],
  CONVERSATION: ["Conservation", ""],
  LAND_SPECULATION: ["Land speculation", "fas fa-chart-line"],
  RENEWABLE_ENERGY: ["Renewable energy", "fas fa-wind"],
  OTHER: ["Other", ""],
};

export const flat_intention_of_investment_map: { [key: string]: string } = {
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

export const confidential_reason_choices = {
  TEMPORARY_REMOVAL: "Temporary removal from PI after criticism",
  RESEARCH_IN_PROGRESS: "Research in progress",
  LAND_OBSERVATORY_IMPORT: "Land Observatory Import",
};
