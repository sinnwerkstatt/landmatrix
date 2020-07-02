export const general_info = [
  {
    name: "Land area",
    fields: [
      {
        name: "country",
        component: "ForeignKeyField",
        label: "Target country",
        model: "country",
      },
      {
        name: "intended_size",
        component: "TextField",
        label: "Intended size (in ha)",
        placeholder: "Size",
        unit: "ha",
      },
      {
        name: "contract_size",
        component: "ValueDateField",
        label: "Size under contract (leased or purchased area, in ha)",
        placeholder: "Size",
        unit: "ha",
      },
      {
        name: "production_size",
        component: "ValueDateField",
        label: "Size in operation (production, in ha)",
        placeholder: "Size",
        unit: "ha",
      },
      {
        name: "land_area_comment",
        component: "TextField",
        label: "Comment on land area",
        multiline: true,
      },
    ],
  },
  {
    name: "Intention of investment",
    fields: [
      {
        name: "intention_of_investment",
        component: "ValueDateField",
        label: "Intention of investment",
        placeholder: "Intention",
        multiselect: {
          multiple: true,
          with_categories: true,
          labels: {
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
            RENEWABLE_ENERGY: "Renewable Energy",
            OTHER: "Other",
          },
          options: [
            {
              category: "Agriculture",
              options: [
                "BIOFUELS",
                "FOOD_CROPS",
                "FODDER",
                "LIVESTOCK",
                "NON_FOOD_AGRICULTURE",
                "AGRICULTURE_UNSPECIFIED",
              ],
            },
            {
              category: "Forestry",
              options: [
                "TIMBER_PLANTATION",
                "FOREST_LOGGING",
                "CARBON",
                "FORESTRY_UNSPECIFIED",
              ],
            },
            {
              category: "Other",
              options: [
                "MINING",
                "OIL_GAS_EXTRACTION",
                "TOURISM",
                "INDUSTRY",
                "CONVERSATION",
                "LAND_SPECULATION",
                "RENEWABLE_ENERGY",
                "OTHER",
              ],
            },
          ],
        },
      },
      {
        name: "intention_of_investment_comment",
        component: "TextField",
        label: "Comment on intention of investment",
        multiline: true,
      },
    ],
  },
  {
    name: "Nature of the deal",
    fields: [
      {
        name: "nature_of_deal",
        component: "CheckboxField",
        label: "Nature of the deal",
        options: {
          OUTRIGHT_PURCHASE: "Outright Purchase",
          LEASE: "Lease",
          CONCESSION: "Concession",
          EXPLOITATION_PERMIT:
            "Exploitation permit / license / concession (for mineral resources)",
          PURE_CONTRACT_FARMING: "Pure contract farming",
        },
      },
      {
        name: "nature_of_deal_comment",
        component: "TextField",
        label: "Comment on the nature of the deal",
        multiline: true,
      },
    ],
  },
  {
    name: "Negotiation status",
    fields: [
      {
        name: "negotiation_status",
        component: "ValueDateField",
        label: "Negotiation status",
        placeholder: "Negotiation status",
        multiselect: {
          multiple: false,
          options: [
            "EXPRESSION_OF_INTEREST",
            "UNDER_NEGOTIATION",
            "MEMORANDUM_OF_UNDERSTANDING",
            "ORAL_AGREEMENT",
            "CONTRACT_SIGNED",
            "NEGOTIATIONS_FAILED",
            "CONTRACT_CANCELED",
            "CONTRACT_EXPIRED",
            "CHANGE_OF_OWNERSHIP",
          ],
          labels: {
            EXPRESSION_OF_INTEREST: "Expression of interest",
            UNDER_NEGOTIATION: "Under negotiation",
            MEMORANDUM_OF_UNDERSTANDING: "Memorandum of understanding",
            ORAL_AGREEMENT: "Oral agreement",
            CONTRACT_SIGNED: "Contract signed",
            NEGOTIATIONS_FAILED: "Negotiations failed",
            CONTRACT_CANCELED: "Contract canceled",
            CONTRACT_EXPIRED: "Contract expired",
            CHANGE_OF_OWNERSHIP: "Change of ownership",
          },
        },
      },
      {
        name: "negotiation_status_comment",
        component: "TextField",
        label: "Comment on negotiation status",
        multiline: true,
      },
    ],
  },
  {
    name: "Implementation status",
    fields: [
      {
        name: "implementation_status",
        component: "ValueDateField",
        label: "Implementation status",
        placeholder: "Implementation status",
        multiselect: {
          multiple: false,
          options: [
            "PROJECT_NOT_STARTED",
            "STARTUP_PHASE",
            "IN_OPERATION",
            "PROJECT_ABANDONED",
          ],
          labels: {
            PROJECT_NOT_STARTED: "Project not started",
            STARTUP_PHASE: "Startup phase (no production)",
            IN_OPERATION: "In operation (production)",
            PROJECT_ABANDONED: "Project abandoned",
          },
        },
      },
      {
        name: "implementation_status_comment",
        component: "TextField",
        label: "Comment on implementation status",
        multiline: true,
      },
    ],
  },
  {
    name: "Purchase price",
    fields: [
      {
        name: "purchase_price",
        component: "DecimalField",
        label: "Purchase price",
      },
      {
        name: "purchase_price_currency",
        component: "ForeignKeyField",
        label: "Purchase price currency",
        model: "currency",
      },
      {
        name: "purchase_price_type",
        component: "TextField",
        label: "Purchase price type",
        model: "currency",
      },
      {
        name: "purchase_price_area",
        component: "DecimalField",
        label: "Purchase price area",
      },
      {
        name: "purchase_price_comment",
        component: "TextField",
        label: "Comment on purchase price",
        multiline: true,
      },
    ],
  },
  {
    name: "Leasing fees",
    fields: [
      {
        name: "annual_leasing_fee",
        component: "DecimalField",
        label: "Annual leasing fee",
      },
      {
        name: "annual_leasing_fee_currency",
        component: "ForeignKeyField",
        label: "Annual leasing fee currency",
        model: "currency",
      },
      {
        name: "annual_leasing_fee_type",
        component: "TextField",
        label: "Annual leasing fee type",
        model: "currency",
      },
      {
        name: "annual_leasing_fee_area",
        component: "DecimalField",
        label: "Annual leasing fee area",
      },
      {
        name: "annual_leasing_fee_comment",
        component: "TextField",
        label: "Comment on annual leasing fee",
        multiline: true,
      },
    ],
  },
  {
    name: "Contract farming",
    fields: [],
  },
];

export const employment = [
  {
    name: "Number of total jobs created",
    fields: [
      {
        name: "total_jobs_created",
        component: "BooleanField",
        label: "Jobs created (total)",
      },
      {
        name: "total_jobs_planned",
        component: "DecimalField",
        label: "Planned number of jobs (total)",
      },
      {
        name: "total_jobs_planned_employees",
        component: "DecimalField",
        label: "Planned employees (total)",
      },
      {
        name: "total_jobs_planned_daily_workers",
        component: "DecimalField",
        label: "Planned daily/seasonal workers (total)",
      },
      {
        name: "total_jobs_current",
        component: "ValueDateField",
        label: "Current number of jobs (total)",
        placeholder: "Amount",
        unit: "jobs",
      },
      {
        name: "total_jobs_current_employees",
        component: "ValueDateField",
        label: "Current number of employees (total)",
        placeholder: "Amount",
        unit: "employees",
      },
      {
        name: "total_jobs_current_daily_workers",
        component: "ValueDateField",
        label: "Current number of daily/seasonal workers (total)",
        placeholder: "Amount",
        unit: "workers",
      },
      {
        name: "total_jobs_created_comment",
        component: "TextField",
        label: "Comment on jobs created (total)",
        multiline: true,
      },
    ],
  },
  {
    name: "Number of jobs for foreigners created",
    fields: [
      {
        name: "foreign_jobs_created",
        component: "BooleanField",
        label: "Jobs created (foreign)",
      },
      {
        name: "foreign_jobs_planned",
        component: "DecimalField",
        label: "Planned number of jobs (foreign)",
      },
      {
        name: "foreign_jobs_planned_employees",
        component: "DecimalField",
        label: "Planned employees (foreign)",
      },
      {
        name: "foreign_jobs_planned_daily_workers",
        component: "DecimalField",
        label: "Planned daily/seasonal workers (foreign)",
      },
      {
        name: "foreign_jobs_current",
        component: "ValueDateField",
        label: "Current number of jobs (foreign)",
        placeholder: "Amount",
        unit: "jobs",
      },
      {
        name: "foreign_jobs_current_employees",
        component: "ValueDateField",
        label: "Current number of employees (foreign)",
        placeholder: "Amount",
        unit: "employees",
      },
      {
        name: "foreign_jobs_current_daily_workers",
        component: "ValueDateField",
        label: "Current number of daily/seasonal workers (foreign)",
        placeholder: "Amount",
        unit: "workers",
      },
      {
        name: "foreign_jobs_created_comment",
        component: "TextField",
        label: "Comment on jobs created (foreign)",
        multiline: true,
      },
    ],
  },
  {
    name: "Number of domestic jobs created",
    fields: [
      {
        name: "domestic_jobs_created",
        component: "BooleanField",
        label: "Jobs created (domestic)",
      },
      {
        name: "domestic_jobs_planned",
        component: "DecimalField",
        label: "Planned number of jobs (domestic)",
      },
      {
        name: "domestic_jobs_planned_employees",
        component: "DecimalField",
        label: "Planned employees (domestic)",
      },
      {
        name: "domestic_jobs_planned_daily_workers",
        component: "DecimalField",
        label: "Planned daily/seasonal workers (domestic)",
      },
      {
        name: "domestic_jobs_current",
        component: "ValueDateField",
        label: "Current number of jobs (domestic)",
        placeholder: "Amount",
        unit: "jobs",
      },
      {
        name: "domestic_jobs_current_employees",
        component: "ValueDateField",
        label: "Current number of employees (domestic)",
        placeholder: "Amount",
        unit: "employees",
      },
      {
        name: "domestic_jobs_current_daily_workers",
        component: "ValueDateField",
        label: "Current number of daily/seasonal workers (domestic)",
        placeholder: "Amount",
        unit: "workers",
      },
      {
        name: "domestic_jobs_created_comment",
        component: "TextField",
        label: "Comment on jobs created (domestic)",
        multiline: true,
      },
    ],
  },
];

export const produce_info = [
  {
    name: "Detailed crop, animal and mineral information",
    fields: [
      {
        name: "crops",
        component: "TextField",
        label: "Crops area/yield/export",
      },
      {
        name: "animals",
        component: "TextField",
        label: "Animals area/yield/export",
      },
      {
        name: "resources",
        component: "TextField",
        label: "Resources area/yield/export",
      },
    ],
  },
];
