export type Section = {
  name: string
  fields: string[]
}

export const getDealSections = ($_: (t: string) => string) => ({
  general_info: [
    {
      name: $_("Land area"),
      fields: [
        "intended_size",
        "contract_size",
        "production_size",
        "land_area_comment",
      ],
    },
    {
      name: $_("Intention of investment"),
      fields: ["intention_of_investment", "intention_of_investment_comment"],
    },
    {
      name: $_("Nature of the deal"),
      fields: ["nature_of_deal", "nature_of_deal_comment"],
    },
    {
      name: $_("Negotiation status"),
      fields: ["negotiation_status", "negotiation_status_comment"],
    },
    {
      name: $_("Implementation status"),
      fields: ["implementation_status", "implementation_status_comment"],
    },
    {
      name: $_("Purchase price"),
      fields: [
        "purchase_price",
        "purchase_price_currency",
        "purchase_price_type",
        "purchase_price_area",
        "purchase_price_comment",
      ],
    },
    {
      name: $_("Leasing fees"),
      fields: [
        "annual_leasing_fee",
        "annual_leasing_fee_currency",
        "annual_leasing_fee_type",
        "annual_leasing_fee_area",
        "annual_leasing_fee_comment",
      ],
    },
    {
      name: $_("Contract farming"),
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
  employment: [
    {
      name: $_("Number of total jobs created"),
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
      name: $_("Number of jobs for foreigners created"),
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
      name: $_("Number of domestic jobs created"),
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
  investor_info: [
    {
      name: $_("Operating company"),
      fields: [
        "operating_company",
        "involved_actors",
        "project_name",
        "investment_chain_comment",
      ],
    },
  ],
  local_communities: [
    {
      name: $_("Names of communities / indigenous peoples affected"),
      fields: [
        "name_of_community",
        "name_of_indigenous_people",
        "people_affected_comment",
      ],
    },
    {
      name: $_("Recognition status of community land tenure"),
      fields: ["recognition_status", "recognition_status_comment"],
    },
    {
      name: $_("Consultation of local community"),
      fields: ["community_consultation", "community_consultation_comment"],
    },
    {
      name: $_("How did the community react?"),
      fields: ["community_reaction", "community_reaction_comment"],
    },
    {
      name: $_("Presence of land conflicts"),
      fields: ["land_conflicts", "land_conflicts_comment"],
    },
    {
      name: $_("Displacement of people"),
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
      name: $_("Negative impacts for local communities"),
      fields: ["negative_impacts", "negative_impacts_comment"],
    },
    {
      name: $_("Promised or received compensation"),
      fields: ["promised_compensation", "received_compensation"],
    },
    {
      name: $_("Promised benefits for local communities"),
      fields: ["promised_benefits", "promised_benefits_comment"],
    },
    {
      name: $_("Materialized benefits for local communities"),
      fields: ["materialized_benefits", "materialized_benefits_comment"],
    },
    {
      name: $_(
        "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
      ),
      fields: ["presence_of_organizations"],
    },
  ],
  former_use: [
    {
      name: $_("Former land owner (not by constitution)"),
      fields: ["former_land_owner", "former_land_owner_comment"],
    },
    {
      name: $_("Former land use"),
      fields: ["former_land_use", "former_land_use_comment"],
    },
    {
      name: $_("Former land cover"),
      fields: ["former_land_cover", "former_land_cover_comment"],
    },
  ],
  produce_info: [
    {
      name: $_("Detailed crop, animal and mineral information"),
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
      name: $_("Detailed contract farming crop and animal information"),
      fields: [
        "contract_farming_crops",
        "contract_farming_crops_comment",
        "contract_farming_animals",
        "contract_farming_animals_comment",
      ],
    },
    {
      name: $_("Use of produce"),
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
      name: $_("In country processing of produce"),
      fields: [
        "in_country_processing",
        "in_country_processing_comment",
        "in_country_processing_facilities",
        "in_country_end_products",
      ],
    },
  ],
  water: [
    {
      name: $_("Water extraction envisaged"),
      fields: ["water_extraction_envisaged", "water_extraction_envisaged_comment"],
    },
    {
      name: $_("Source of water extraction"),
      fields: ["source_of_water_extraction", "source_of_water_extraction_comment"],
    },
    {
      name: $_(
        "How much do investors pay for water and the use of water infrastructure?",
      ),
      fields: ["how_much_do_investors_pay_comment"],
    },
    {
      name: $_("How much water is extracted?"),
      fields: [
        "water_extraction_amount",
        "water_extraction_amount_comment",
        "use_of_irrigation_infrastructure",
        "use_of_irrigation_infrastructure_comment",
        "water_footprint",
      ],
    },
  ],
  gender_related_info: [
    {
      name: $_("Any gender-specific information about the investment and its impacts"),
      fields: ["gender_related_information"],
    },
  ],
  overall_comment: [
    {
      name: $_("Overall comment"),
      fields: ["overall_comment"],
    },
  ],
  meta: [
    {
      name: $_("Fully updated"),
      fields: ["fully_updated"],
    },
    {
      name: $_("Confidential"),
      fields: ["confidential", "confidential_comment"],
    },
  ],
})

export const subsections = {
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
  involvement: [
    "investor",
    "investment_type",
    "percentage",
    "loans_amount",
    "loans_currency",
    "loans_date",
    "parent_relation",
    "comment",
  ],
}

export const getInvestorSections = ($_: (t: string) => string) => ({
  general_info: [
    {
      name: $_("General Info"),
      fields: [
        "name",
        "country",
        "classification",
        "homepage",
        "opencorporates",
        "comment",
      ],
    },
  ],
})

// export const investorSubsections = {
//   parent_companies: [
//     "investor",
//     "investment_type",
//     "percentage",
//     "loans_amount",
//     "loans_currency",
//     "loans_date",
//     "comment",
//   ],
//   tertiary_investors: [
//     "investor",
//     "investment_type",
//     "ownership_share",
//     "loan_amount",
//     "loan_currency",
//     "loan_date",
//     "parent_relation",
//     "comment",
//   ],
// };
