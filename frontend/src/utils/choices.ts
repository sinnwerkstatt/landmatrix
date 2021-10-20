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

export const combined_status_options: { [key: string]: string } = {
  DRAFT: "Draft", // status==1
  REVIEW: "Submitted for Review", // status==1, draft_status == 2
  ACTIVATION: "Submitted for Activation", // status==1, draft_status == 3
  LIVE: "Live", // status == 2 || status == 3
  LIVE_AND_DRAFT: "Live + Draft", // (status == 2 || status == 3) || draft_status != null
  DELETED: "Deleted", // status ==4
};

export const combined_status_fn = (
  status: number,
  draft_status: number,
  toString = false
): string => {
  let ret;
  if (status === 1 && draft_status === 1) ret = "DRAFT";
  if (status === 1 && draft_status === 2) ret = "REVIEW";
  if (status === 1 && draft_status === 3) ret = "ACTIVATION";
  if (status === 1 && draft_status === 4) ret = "UNCLEAR. 1 4 ??";
  if ([2, 3].includes(status) && draft_status === null) ret = "LIVE";
  if ([2, 3].includes(status) && draft_status !== null) ret = "LIVE_AND_DRAFT";
  if (status === 4) ret = "DELETED";
  if (!ret) throw Error(`Invalid status ${status} ${draft_status}`);
  return toString ? combined_status_options[ret] : ret;
};

export const confidential_reason_choices = {
  TEMPORARY_REMOVAL: "Temporary removal from PI after criticism",
  RESEARCH_IN_PROGRESS: "Research in progress",
  LAND_OBSERVATORY_IMPORT: "Land Observatory Import",
};
