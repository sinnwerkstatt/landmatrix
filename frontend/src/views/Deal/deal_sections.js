export const deal_sections = {
  general_info: {
    label: "General info",
    subsections: [
      {
        name: "Land area",
        fields: [
          "intended_size",
          "contract_size",
          "production_size",
          "land_area_comment",
        ],
      },
      {
        name: "Intention of investment",
        fields: ["intention_of_investment", "intention_of_investment_comment"],
      },
      {
        name: "Nature of the deal",
        fields: ["nature_of_deal", "nature_of_deal_comment"],
      },
      {
        name: "Negotiation status",
        fields: ["negotiation_status", "negotiation_status_comment"],
      },
      {
        name: "Implementation status",
        fields: ["implementation_status", "implementation_status_comment"],
      },
      {
        name: "Purchase price",
        fields: [
          "purchase_price",
          "purchase_price_currency",
          "purchase_price_type",
          "purchase_price_area",
          "purchase_price_comment",
        ],
      },
      {
        name: "Leasing fees",
        fields: [
          "annual_leasing_fee",
          "annual_leasing_fee_currency",
          "annual_leasing_fee_type",
          "annual_leasing_fee_area",
          "annual_leasing_fee_comment",
        ],
      },
      {
        name: "Contract farming",
        fields: [
          "contract_farming",
          "on_the_lease_state",
          "on_the_lease",
          "off_the_lease_state",
          "off_the_lease",
          "contract_farming_comment",
        ],
      },
    ],
  },
  employment: {
    label: "Employment",
    subsections: [
      {
        name: "Number of total jobs created",
        fields: [
          "total_jobs_created",
          "total_jobs_planned",
          "total_jobs_planned_employees",
          "total_jobs_planned_daily_workers",
          "total_jobs_current",
          "total_jobs_created_comment",
        ],
      },
      {
        name: "Number of jobs for foreigners created",
        fields: [
          "foreign_jobs_created",
          "foreign_jobs_planned",
          "foreign_jobs_planned_employees",
          "foreign_jobs_planned_daily_workers",
          "foreign_jobs_current",
          "foreign_jobs_created_comment",
        ],
      },
      {
        name: "Number of domestic jobs created",
        fields: [
          "domestic_jobs_created",
          "domestic_jobs_planned",
          "domestic_jobs_planned_employees",
          "domestic_jobs_planned_daily_workers",
          "domestic_jobs_current",
          "domestic_jobs_created_comment",
        ],
      },
    ],
  },
  investor_info: {
    label: "Investor info",
    subsections: [
      {
        name: "Operating company",
        fields: [
          "operating_company",
          "involved_actors",
          "project_name",
          "investment_chain_comment",
        ],
      },
    ],
  },
  local_communities: {
    label: "Local communities / indigenous peoples",
    subsections: [
      {
        name: "Names of communities / indigenous peoples affected",
        fields: [
          "name_of_community",
          "name_of_indigenous_people",
          "people_affected_comment",
        ],
      },
      {
        name: "Recognition status of community land tenure",
        fields: ["recognition_status", "recognition_status_comment"],
      },
      {
        name: "Consultation of local community",
        fields: ["community_consultation", "community_consultation_comment"],
      },
      {
        name: "How did the community react?",
        fields: ["community_reaction", "community_reaction_comment"],
      },
      {
        name: "Presence of land conflicts",
        fields: ["land_conflicts", "land_conflicts_comment"],
      },
      {
        name: "Displacement of people",
        fields: [
          "displacement_of_people",
          "displaced_people",
          "displaced_households",
          "displaced_people_from_community_land",
          "displaced_people_within_community_land",
          "displaced_households_from_fields",
          "displaced_people_on_completion",
          "displacement_of_people_comment",
        ],
      },
      {
        name: "Negative impacts for local communities",
        fields: ["negative_impacts", "negative_impacts_comment"],
      },
      {
        name: "Promised or received compensation",
        fields: ["promised_compensation", "received_compensation"],
      },
      {
        name: "Promised benefits for local communities",
        fields: ["promised_benefits", "promised_benefits_comment"],
      },
      {
        name: "Materialized benefits for local communities",
        fields: ["materialized_benefits", "materialized_benefits_comment"],
      },
      {
        name: "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
        fields: ["presence_of_organizations"],
      },
    ],
  },
  former_use: {
    label: "Former use",
    subsections: [
      {
        name: "Former land owner (not by constitution)",
        fields: ["former_land_owner", "former_land_owner_comment"],
      },
      {
        name: "Former land use",
        fields: ["former_land_use", "former_land_use_comment"],
      },
      {
        name: "Former land cover",
        fields: ["former_land_cover", "former_land_cover_comment"],
      },
    ],
  },
  produce_info: {
    label: "Produce info",
    subsections: [
      {
        name: "Detailed crop, animal and mineral information",
        fields: [
          "crops",
          "crops_comment",
          "animals",
          "animals_comment",
          "mineral_resources",
          "mineral_resources_comment",
        ],
      },
      {
        name: "Detailed contract farming crop and animal information",
        fields: [
          "contract_farming_crops",
          "contract_farming_crops_comment",
          "contract_farming_animals",
          "contract_farming_animals_comment",
        ],
      },
      {
        name: "Use of produce",
        fields: [
          "has_domestic_use",
          "domestic_use",
          "has_export",
          "export",
          "export_country1",
          "export_country1_ratio",
          "export_country2",
          "export_country2_ratio",
          "export_country3",
          "export_country3_ratio",
          "use_of_produce_comment",
        ],
      },
      {
        name: "In country processing of produce",
        fields: [
          "in_country_processing",
          "in_country_processing_comment",
          "in_country_processing_facilities",
          "in_country_end_products",
        ],
      },
    ],
  },
  water: {
    label: "Water",
    subsections: [
      {
        name: "Water extraction envisaged",
        fields: ["water_extraction_envisaged", "water_extraction_envisaged_comment"],
      },
      {
        name: "Source of water extraction",
        fields: ["source_of_water_extraction", "source_of_water_extraction_comment"],
      },
      {
        name: "How much do investors pay for water and the use of water infrastructure?",
        fields: ["how_much_do_investors_pay_comment"],
      },
      {
        name: "How much water is extracted?",
        fields: [
          "water_extraction_amount",
          "water_extraction_amount_comment",
          "use_of_irrigation_infrastructure",
          "use_of_irrigation_infrastructure_comment",
          "water_footprint",
        ],
      },
    ],
  },
  gender_related_info: {
    label: "Gender-related info",
    subsections: [
      {
        name: "Any gender-specific information about the investment and its impacts",
        fields: ["gender_related_information"],
      },
    ],
  },
  guidelines_and_principles: {
    label: "Guidelines & Principles",
    subsections: [
      {
        name: "Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)",
        fields: ["vggt_applied", "vggt_applied_comment"],
      },
      {
        name: "Principles for Responsible Agricultural Investments (PRAI)",
        fields: ["prai_applied", "prai_applied_comment"],
      },
    ],
  },
  overall_comment: {
    label: "Overall comment",
    subsections: [
      {
        name: "Overall comment",
        fields: ["overall_comment"],
      },
    ],
  },
  meta: {
    label: "Meta",
    subsections: [
      {
        name: "Fully updated",
        fields: ["fully_updated"],
      },
      {
        name: "Confidential",
        fields: ["confidential", "confidential_reason", "confidential_comment"],
      },
    ],
  },
};

export const deal_submodel_sections = {
  location: [
    "level_of_accuracy",
    "name",
    "description",
    "point",
    "facility_name",
    "comment",
  ],
  contract: ["number", "date", "expiration_date", "agreement_duration", "comment"],
  datasource: [
    "type",
    "url",
    "file",
    "file_not_public",
    "publication_title",
    "date",
    "name",
    "company",
    "email",
    "phone",
    "includes_in_country_verified_information",
    "open_land_contracts_id",
    "comment",
  ],
};
