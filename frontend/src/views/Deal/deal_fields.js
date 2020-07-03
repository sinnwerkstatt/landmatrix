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
    fields: [
      {
        name: "contract_farming",
        component: "BooleanField",
        label: "Contract farming",
      },
      {
        name: "on_the_lease",
        component: "BooleanField",
        label: "On leased / purchased area",
      },
      {
        name: "on_the_lease_area",
        component: "ValueDateField",
        label: "On leased / purchased area (in ha)",
        placeholder: "Area",
        unit: "ha",
      },
      {
        name: "on_the_lease_farmers",
        component: "ValueDateField",
        label: "On leased / purchased farmers",
        placeholder: "",
        unit: "farmers",
      },
      {
        name: "on_the_lease_households",
        component: "ValueDateField",
        label: "On leased / purchased households",
        placeholder: "",
        unit: "households",
      },

      {
        name: "off_the_lease",
        component: "BooleanField",
        label: "Not on leased / purchased area (out-grower)",
      },

      {
        name: "off_the_lease_area",
        component: "ValueDateField",
        label: "Not on leased / purchased area (out-grower, in ha)",
        placeholder: "Area",
        unit: "ha",
      },
      {
        name: "off_the_lease_farmers",
        component: "ValueDateField",
        label: "Not on leased / purchased farmers (out-grower)",
        placeholder: "",
        unit: "farmers",
      },
      {
        name: "off_the_lease_households",
        component: "ValueDateField",
        label: "Not on leased / purchased households (out-grower)",
        placeholder: "",
        unit: "households",
      },
      {
        name: "contract_farming_comment",
        component: "TextField",
        label: "Comment on contract farming",
        multiline: true,
      },
    ],
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

export const investor_info = [
  {
    name: "Operating company",
    fields: [
      {
        name: "operating_company",
        component: "ForeignKeyField",
        label: "Operating company",
        model: "investor",
      },
      {
        name: "involved_actors",
        component: "ValueDateField", // need to change this field
        label: "Actors involved in the negotiation / admission process",
        unit: "role",
      },
      {
        name: "project_name",
        component: "TextField",
        label: "Name of investment project",
      },
      {
        name: "investment_chain_comment",
        component: "TextField",
        label: "Comment on investment chain",
        multiline: true,
      },
    ],
  },
];

export const local_communities_info = [
  {
    name: "Names of communities / indigenous peoples affected",
    fields: [
      {
        name: "name_of_community",
        component: "TextField",
        label: "Name of community",
      },
      {
        name: "name_of_indigenous_people",
        component: "TextField",
        label: "Name of indigenous people",
      },
      {
        name: "people_affected_comment",
        component: "TextField",
        label: "Comment on communities / indigenous peoples affected",
        multiline: true,
      },
    ],
  },
  {
    name: "Recognitions status of community land tenure",
    fields: [
      {
        name: "recognition_status",
        component: "CheckboxField",
        label: "Recognition status",
        options: {
          INDIGENOUS_RIGHTS_RECOGNIZED:
            "Indigenous Peoples traditional or customary rights recognized by government",
          INDIGENOUS_RIGHTS_NOT_RECOGNIZED:
            "Indigenous Peoples traditional or customary rights not recognized by government",
          COMMUNITY_RIGHTS_RECOGNIZED:
            "Community traditional or customary rights recognized by government",
          COMMUNITY_RIGHTS_NOT_RECOGNIZED:
            "Community traditional or customary rights not recognized by government",
        },
      },
      {
        name: "recognition_status_comment",
        component: "TextField",
        label: "Comment on recognitions status of community land tenure",
        multiline: true,
      },
    ],
  },
  {
    name: "Consultation of local community",
    fields: [
      {
        name: "community_consultation",
        component: "TextField",
        label: "Community consultation",
      },
      {
        name: "community_consultation_comment",
        component: "TextField",
        label: "Comment on consultation of local community",
        multiline: true,
      },
    ],
  },
  {
    name: "How did the community react?",
    fields: [
      {
        name: "community_reaction",
        component: "TextField",
        label: "Community reaction",
      },
      {
        name: "community_reaction_comment",
        component: "TextField",
        label: "Comment on community reaction",
        multiline: true,
      },
    ],
  },
  {
    name: "Presence of land conflicts",
    fields: [
      {
        name: "land_conflicts",
        component: "BooleanField",
        label: "Presence of land conflicts",
      },
      {
        name: "land_conflicts_comment",
        component: "TextField",
        label: "Comment on presence of land conflicts",
        multiline: true,
      },
    ],
  },
  {
    name: "Displacement of people",
    fields: [
      {
        name: "displacement_of_people",
        component: "BooleanField",
        label: "Displacement of people",
      },
      {
        name: "displaced_people",
        component: "DecimalField",
        label: "Number of people actually displaced",
      },
      {
        name: "displaced_households",
        component: "DecimalField",
        label: "Number of households actually displaced",
      },
      {
        name: "displaced_people_from_community_land",
        component: "DecimalField",
        label: "Number of people displaced out of their community land",
      },
      {
        name: "displaced_people_within_community_land",
        component: "DecimalField",
        label: "Number of people displaced staying on community land",
      },
      {
        name: "displaced_households_from_fields",
        component: "DecimalField",
        label: 'Number of households displaced "only" from their agricultural fields',
      },
      {
        name: "displaced_people_on_completion",
        component: "DecimalField",
        label: "Number of people facing displacement once project is fully implemented",
      },
      {
        name: "displacement_of_people_comment",
        component: "TextField",
        label: "Comment on presence of land conflicts",
        multiline: true,
      },
    ],
  },
  {
    name: "Negative impacts for local communities",
    fields: [
      {
        name: "negative_impacts",
        component: "TextField",
        label: "Negative impacts for local communities",
      },
      {
        name: "negative_impacts_comment",
        component: "TextField",
        label: "Comment on negative impacts for local communities",
        multiline: true,
      },
    ],
  },
  {
    name: "Promised or received compensation",
    fields: [
      {
        name: "promised_compensation",
        component: "TextField",
        label: "Promised compensation (e.g. for damages or resettlements)",
        multiline: true,
      },
      {
        name: "received_compensation",
        component: "TextField",
        label: "Received compensation (e.g. for damages or resettlements)",
        multiline: true,
      },
    ],
  },
  {
    name: "Promised benefits for local communities",
    fields: [
      {
        name: "promised_benefits",
        component: "TextField",
        label: "Promised compensation (e.g. for damages or resettlements)",
        multiline: true,
      },
      {
        name: "promised_benefits_comment",
        component: "TextField",
        label: "Received compensation (e.g. for damages or resettlements)",
        multiline: true,
      },
    ],
  },
  {
    name: "Materialized benefits for local communities",
    fields: [
      {
        name: "materialized_benefits",
        component: "TextField",
        label: "Materialized benefits for local communities",
        multiline: true,
      },
      {
        name: "materialized_benefits_comment",
        component: "TextField",
        label: "Comment on materialized benefits for local communities",
        multiline: true,
      },
    ],
  },
  {
    name:
      "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
    fields: [
      {
        name: "presence_of_organizations",
        component: "TextField",
        label:
          "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
        multiline: true,
      },
    ],
  },
];

export const former_use = [
  {
    name: "Former land owner (not by constitution)",
    fields: [
      {
        name: "former_land_owner",
        component: "TextField",
        label: "Former land owner",
      },
      {
        name: "former_land_owner_comment",
        component: "TextField",
        label: "Comment on former land owner",
        multiline: true,
      },
    ],
  },
  {
    name: "Former land use",
    fields: [
      {
        name: "former_land_use",
        component: "TextField",
        label: "Former land use",
      },
      {
        name: "former_land_use_comment",
        component: "TextField",
        label: "Comment on former land use",
        multiline: true,
      },
    ],
  },
  {
    name: "Former land cover",
    fields: [
      {
        name: "former_land_cover",
        component: "TextField",
        label: "Former land cover",
      },
      {
        name: "former_land_cover_comment",
        component: "TextField",
        label: "Comment on former land cover",
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
        name: "crops_comment",
        component: "TextField",
        label: "Comment on crops",
        multiline: true,
      },
      {
        name: "animals",
        component: "TextField",
        label: "Animals area/yield/export",
      },
      {
        name: "animals_comment",
        component: "TextField",
        label: "Comment on animals",
        multiline: true,
      },
      {
        name: "resources",
        component: "TextField",
        label: "Resources area/yield/export",
      },
      {
        name: "resources_comment",
        component: "TextField",
        label: "Comment on resources",
        multiline: true,
      },
    ],
  },
  {
    name: "Detailed contract farming crop and animal information",
    fields: [
      {
        name: "contract_farming_crops",
        component: "TextField",
        label: "Contract farming crops",
      },
      {
        name: "contract_farming_crops_comment",
        component: "TextField",
        label: "Comment on contract farming crops",
        multiline: true,
      },
      {
        name: "contract_farming_animals",
        component: "TextField",
        label: "Contract farming animals",
      },
      {
        name: "contract_farming_animals_comment",
        component: "TextField",
        label: "Comment on contract farming animals",
        multiline: true,
      },
    ],
  },
  {
    name: "Use of produce",
    fields: [
      {
        name: "has_domestic_use",
        component: "BooleanField",
        label: "Has domestic use",
      },
      {
        name: "domestic_use",
        component: "DecimalField",
        label: "Ownership share",
      },
      {
        name: "has_export",
        component: "BooleanField",
        label: "Has export",
      },
      {
        name: "export_country1",
        component: "ForeignKeyField",
        label: "Country 1",
        model: "country",
      },
      {
        name: "export_country1_ratio",
        component: "DecimalField",
        label: "Country 1 ratio",
      },
      {
        name: "export_country2",
        component: "ForeignKeyField",
        label: "Country 2",
        model: "country",
      },
      {
        name: "export_country2_ratio",
        component: "DecimalField",
        label: "Country 2 ratio",
      },
      {
        name: "export_country3",
        component: "ForeignKeyField",
        label: "Country 3",
        model: "country",
      },
      {
        name: "export_country3_ratio",
        component: "DecimalField",
        label: "Country 3 ratio",
      },
      {
        name: "use_of_produce_comment",
        component: "TextField",
        label: "Comment on use of produce",
        multiline: true,
      },
    ],
  },
  {
    name: "In country processing of produce",
    fields: [
      {
        name: "in_country_processing",
        component: "BooleanField",
        label: "In country processing of produce",
      },
      {
        name: "in_country_processing_comment",
        component: "TextField",
        label: "Comment on in country processing of produce",
        multiline: true,
      },
      {
        name: "in_country_processing_facilities",
        component: "TextField",
        label:
          "Processing facilities / production infrastructure of the project (e.g. oil mill, ethanol distillery, biomass power plant etc.)",
        multiline: true,
      },
      {
        name: "in_country_end_products",
        component: "TextField",
        label: "In-country end products of the project",
        multiline: true,
      },
    ],
  },
];

export const water = [
  {
    name: "Water extraction envisaged",
    fields: [
      {
        name: "water_extraction_envisaged",
        component: "BooleanField",
        label: "Water extraction envisaged",
      },
      {
        name: "water_extraction_envisaged_comment",
        component: "TextField",
        label: "Comment on water extraction envisaged",
        multiline: true,
      },
    ],
  },
  {
    name: "Source of water extraction",
    fields: [
      {
        name: "source_of_water_extraction",
        component: "TextField",
        label: "Source of water extraction",
      },
      {
        name: "source_of_water_extraction_comment",
        component: "TextField",
        label: "Comment on source of water extraction",
        multiline: true,
      },
    ],
  },
  {
    name: "How much do investors pay for water and the use of water infrastructure?\n",
    fields: [
      {
        name: "how_much_do_investors_pay_comment",
        component: "TextField",
        label: "Comment on how much do investors pay for water",
        multiline: true,
      },
    ],
  },
  {
    name: "How much water is extracted?",
    fields: [
      {
        name: "water_extraction_amount",
        component: "DecimalField",
        label: "Water extraction amount",
      },
      {
        name: "water_extraction_amount_comment",
        component: "TextField",
        label: "Comment on how much water is extracted",
        multiline: true,
      },
      {
        name: "use_of_irrigation_infrastructure",
        component: "BooleanField",
        label: "Use of irrigation infrastructure",
      },
      {
        name: "use_of_irrigation_infrastructure_comment",
        component: "TextField",
        label: "Comment on use of irrigation infrastructure",
        multiline: true,
      },
      {
        name: "water_footprint",
        component: "TextField",
        label: "Water footprint of the investment project",
        multiline: true,
      },
    ],
  },
];

export const gender_related_info = [
  {
    name: "Any gender-specific information about the investment and its impacts",
    fields: [
      {
        name: "gender_related_information",
        component: "TextField",
        label: "Gender-related information",
        multiline: true,
      },
    ],
  },
];

export const guidelines_and_principles = [
  {
    name: "Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)",
    fields: [
      {
        name: "vggt_applied",
        component: "TextField",
        label:
          "Application of Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)",
      },
      {
        name: "vggt_applied_comment",
        component: "TextField",
        label: "Comment on VGGT",
        multiline: true,
      },
    ],
  },
  {
    name: "Principles for Responsible Agricultural Investments (PRAI)",
    fields: [
      {
        name: "prai_applied",
        component: "TextField",
        label:
          "Application of Principles for Responsible Agricultural Investments (PRAI)",
      },
      {
        name: "prai_applied_comment",
        component: "TextField",
        label: "Comment on PRAI",
        multiline: true,
      },
    ],
  },
];
