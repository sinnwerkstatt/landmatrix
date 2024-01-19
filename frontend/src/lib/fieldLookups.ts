import type { ComponentType } from "svelte"
import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import { fieldChoices } from "$lib/stores"

import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
import ChoicesField from "$components/Fields/Display2/ChoicesField.svelte"
import CountryField from "$components/Fields/Display2/CountryField.svelte"
import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
import IDField from "$components/Fields/Display2/IDField.svelte"
import InvestorLinkField from "$components/Fields/Display2/InvestorLinkField.svelte"
import IOIField from "$components/Fields/Display2/IOIField.svelte"
import JSONActorsField from "$components/Fields/Display2/JSONActorsField.svelte"
import JSONCarbonSequestrationField from "$components/Fields/Display2/JSONCarbonSequestrationField.svelte"
import JSONCurrentDateAreaChoicesField from "$components/Fields/Display2/JSONCurrentDateAreaChoicesField.svelte"
import JSONCurrentDateAreaField from "$components/Fields/Display2/JSONCurrentDateAreaField.svelte"
import JSONCurrentDateChoiceField from "$components/Fields/Display2/JSONCurrentDateChoiceField.svelte"
import JSONElectricityGenerationField from "$components/Fields/Display2/JSONElectricityGenerationField.svelte"
import JSONExportsField from "$components/Fields/Display2/JSONExportsField.svelte"
import JSONJobsField from "$components/Fields/Display2/JSONJobsField.svelte"
import JSONLeaseField from "$components/Fields/Display2/JSONLeaseField.svelte"
import NanoIDField from "$components/Fields/Display2/NanoIDField.svelte"
import PointField from "$components/Fields/Display2/PointField.svelte"
import TextField from "$components/Fields/Display2/TextField.svelte"
import UserField from "$components/Fields/Display2/UserField.svelte"

interface Sec {
  displayField: ComponentType
  label: string
  extras?: unknown
}

export const investorFields = derived([_, fieldChoices], ([$_, $fieldChoices]) => {
  return {
    id: { displayField: IDField, label: $_("ID"), extras: { model: "investor" } },

    country: {
      displayField: CountryField,
      label: $_("Country of registration/origin"),
    },
    name: { displayField: TextField, label: $_("Name") },
    homepage: { displayField: TextField, label: $_("Investor homepage") },
    comment: { displayField: TextField, label: $_("Comment") },
    opencorporates: { displayField: TextField, label: $_("Opencorporates link") },
    classification: {
      displayField: ChoicesField,
      label: $_("Classification"),
      extras: { choices: $fieldChoices.investor.classification },
    },
  } as { [key: string]: Sec }
})

export const dealSections = derived(_, $_ => {
  return {
    land_area: {
      title: $_("Land area"),
      fields: [
        "intended_size",
        "contract_size",
        "production_size",
        "land_area_comment",
      ],
    },
    intention_of_investment: {
      title: $_("Intention of investment"),
      fields: ["intention_of_investment", "intention_of_investment_comment"],
    },
    nature_of_deal: {
      title: $_("Nature of the deal"),
      fields: ["nature_of_deal", "nature_of_deal_comment"],
    },
    negotiation_status: {
      title: $_("Negotiation status"),
      fields: ["negotiation_status", "negotiation_status_comment"],
    },
    implementation_status: {
      title: $_("Implementation status"),
      fields: ["implementation_status", "implementation_status_comment"],
    },
    purchase_price: {
      title: $_("Purchase price"),
      fields: ["purchase_price", "purchase_price_area", "purchase_price_comment"],
    },
    leasing_fee: {
      title: $_("Leasing fees"),
      fields: [
        "annual_leasing_fee",
        "annual_leasing_fee_area",
        "annual_leasing_fee_comment",
      ],
    },
    contract_farming: {
      title: $_("Contract farming"),
      fields: [
        "contract_farming",
        "on_the_lease_state",
        "on_the_lease",
        "off_the_lease_state",
        "off_the_lease",
        "contract_farming_comment",
      ],
    },
    // EMPLOYMENT
    total_jobs_created: {
      title: $_("Number of total jobs created"),
      fields: [
        "total_jobs_created",
        "total_jobs_planned",
        "total_jobs_planned_employees",
        "total_jobs_planned_daily_workers",
        "total_jobs_current",
        "total_jobs_created_comment",
      ],
    },
    foreign_jobs_created: {
      title: $_("Number of jobs for foreigners created"),
      fields: [
        "foreign_jobs_created",
        "foreign_jobs_planned",
        "foreign_jobs_planned_employees",
        "foreign_jobs_planned_daily_workers",
        "foreign_jobs_current",
        "foreign_jobs_created_comment",
      ],
    },
    domestic_jobs_created: {
      title: $_("Number of domestic jobs created"),
      fields: [
        "domestic_jobs_created",
        "domestic_jobs_planned",
        "domestic_jobs_planned_employees",
        "domestic_jobs_planned_daily_workers",
        "domestic_jobs_current",
        "domestic_jobs_created_comment",
      ],
    },
    // Investor Info
    operating_company: {
      title: $_("Operating Company"),
      fields: [
        "operating_company_id",
        "involved_actors",
        "project_name",
        "investment_chain_comment",
      ],
    },
    // Local communities
    name_of_community: {
      title: $_("Names of communities / indigenous peoples affected"),
      fields: [
        "name_of_community",
        "name_of_indigenous_people",
        "people_affected_comment",
      ],
    },
    recognition_status: {
      title: $_("Recognition status of community land tenure"),
      fields: ["recognition_status", "recognition_status_comment"],
    },
    community_consultation: {
      title: $_("Consultation of local community"),
      fields: ["community_consultation", "community_consultation_comment"],
    },
    community_reaction: {
      title: $_("How did the community react?"),
      fields: ["community_reaction", "community_reaction_comment"],
    },
    land_conflicts: {
      title: $_("Presence of land conflicts"),
      fields: ["land_conflicts", "land_conflicts_comment"],
    },
    displaced_people: {
      title: $_("Displacement of people"),
      fields: [
        "displaced_people",
        "displaced_households",
        "displaced_people_from_community_land",
        "displaced_people_within_community_land",
        "displaced_households_from_fields",
        "displaced_people_on_completion",
        "displacement_of_people_comment",
      ],
    },
    negative_impacts: {
      title: $_("Negative impacts for local communities"),
      fields: ["negative_impacts", "negative_impacts_comment"],
    },
    promised_compensation: {
      title: $_("Promised or received compensation"),
      fields: ["promised_compensation", "received_compensation"],
    },
    promised_benefits: {
      title: $_("Promised benefits for local communities"),
      fields: ["promised_benefits", "promised_benefits_comment"],
    },
    materialized_benefits: {
      title: $_("Materialized benefits for local communities"),
      fields: ["materialized_benefits", "materialized_benefits_comment"],
    },
    presence_of_organizations: {
      title: $_(
        "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
      ),
      fields: ["presence_of_organizations"],
    },
    // Former Use
    former_land_owner: {
      title: $_("Former land owner (not by constitution)"),
      fields: ["former_land_owner", "former_land_owner_comment"],
    },
    former_land_use: {
      title: $_("Former land use"),
      fields: ["former_land_use", "former_land_use_comment"],
    },
    former_land_cover: {
      title: $_("Former land cover"),
      fields: ["former_land_cover", "former_land_cover_comment"],
    },
    // Produce info
    farming: {
      title: $_("Detailed crop, animal and mineral information"),
      fields: [
        "crops",
        "crops_comment",
        "animals",
        "animals_comment",
        "mineral_resources",
        "mineral_resources_comment",
      ],
    },
    //  TODO doulbe contract farming?!
    contract_farming2: {
      title: $_("Detailed contract farming crop and animal information"),
      fields: [
        "contract_farming_crops",
        "contract_farming_crops_comment",
        "contract_farming_animals",
        "contract_farming_animals_comment",
      ],
    },
    electricity_generation: {
      title: $_("Detailed electricity generation information"),
      fields: ["electricity_generation", "electricity_generation_comment"],
    },
    carbon_sequestration: {
      title: $_("Detailed carbon sequestration information"),
      fields: ["carbon_sequestration", "carbon_sequestration_comment"],
    },
    use_of_produce: {
      title: $_("Use of produce"),
      fields: [
        "domestic_use",
        "export",
        "export_country1",
        "export_country1_ratio",
        "export_country2",
        "export_country2_ratio",
        "export_country3",
        "export_country3_ratio",
      ],
    },
    in_country_processing: {
      title: $_("In country processing of produce"),
      fields: [
        "in_country_processing",
        "in_country_processing_comment",
        "in_country_processing_facilities",
        "in_country_end_products",
      ],
    },
    // Water
    water_extraction_envisaged: {
      title: $_("Water extraction envisaged"),
      fields: ["water_extraction_envisaged", "water_extraction_envisaged_comment"],
    },
    source_of_water_extraction: {
      title: $_("Source of water extraction"),
      fields: ["source_of_water_extraction", "source_of_water_extraction_comment"],
    },
    how_much_do_investors_pay_comment: {
      title: $_(
        "How much do investors pay for water and the use of water infrastructure?",
      ),
      fields: ["how_much_do_investors_pay_comment"],
    },
    water_extraction_amount: {
      title: $_("How much water is extracted?"),
      fields: [
        "water_extraction_amount",
        "water_extraction_amount_comment",
        "use_of_irrigation_infrastructure",
        "use_of_irrigation_infrastructure_comment",
        "water_footprint",
      ],
    },
    // Gender
    gender_related_information: {
      title: $_("Any gender-specific information about the investment and its impacts"),
      fields: ["gender_related_information"],
    },
    // Overall comment
    overall_comment: {
      title: $_("Overall comment"),
      fields: ["overall_comment"],
    },
  } as { [key: string]: { title: string; fields: string[] } }
})

export const dealFields = derived([_, fieldChoices], ([$_, $fieldChoices]) => {
  return {
    // // Deal Hull
    id: { displayField: IDField, label: $_("ID") },
    country: { displayField: CountryField, label: $_("Target country") },
    country_id: { displayField: CountryField, label: $_("Target country") },
    confidential: { displayField: BooleanField, label: $_("Confidential") },
    created_at: { displayField: DateTimeField, label: $_("Created at") },
    created_by_id: { displayField: UserField, label: $_("Created by") },
    modified_at: { displayField: DateTimeField, label: $_("Modified at") },
    modified_by_id: { displayField: UserField, label: $_("Modified by") },
    fully_updated_at: { displayField: DateTimeField, label: $_("Last full update") },
    // General
    intended_size: {
      displayField: DecimalField,
      label: $_("Intended size"),
      extras: { unit: $_("ha") },
    },
    contract_size: {
      displayField: JSONCurrentDateAreaField,
      label: $_("Size under contract (leased or purchased area)"),
    },
    production_size: {
      displayField: JSONCurrentDateAreaField,
      label: $_("Size in operation (production)"),
    },
    land_area_comment: {
      displayField: TextField,
      label: $_("Comment on land area"),
    },
    intention_of_investment: {
      displayField: JSONCurrentDateAreaChoicesField,
      label: $_("Intention of investment"),
      extras: { choices: $fieldChoices.deal.intention_of_investment },
    },
    intention_of_investment_comment: {
      displayField: TextField,
      label: $_("Comment on intention of investment"),
    },
    nature_of_deal: {
      displayField: ChoicesField,
      label: $_("Nature of the deal"),
      extras: { choices: $fieldChoices.deal.nature_of_deal, multipleChoices: true },
    },
    nature_of_deal_comment: {
      displayField: TextField,
      label: $_("Comment on nature of the deal"),
    },
    negotiation_status: {
      displayField: JSONCurrentDateChoiceField,
      label: $_("Negotiation status"),
      extras: { choices: $fieldChoices.deal.negotiation_status },
    },
    negotiation_status_comment: {
      displayField: TextField,
      label: $_("Comment on negotiation status"),
    },
    implementation_status: {
      displayField: JSONCurrentDateChoiceField,
      label: $_("Implementation status"),
      extras: {
        choices: $fieldChoices.deal.implementation_status,
      },
    },
    implementation_status_comment: {
      displayField: TextField,
      label: $_("Comment on implementation status"),
    },
    purchase_price: {
      displayField: DecimalField,
      label: $_("Purchase price"),
      // we use purchase_price_currency and purchase_price_type here too
    },
    purchase_price_area: {
      displayField: DecimalField,
      label: $_("Purchase price area"),
      extras: { unit: $_("ha") },
    },
    purchase_price_comment: {
      displayField: TextField,
      label: $_("Comment on purchase price"),
    },
    annual_leasing_fee: {
      displayField: DecimalField,
      label: $_("Annual leasing fee"),
      // we use annual_leasing_fee_currency and ~_type here too
    },
    annual_leasing_fee_area: {
      displayField: DecimalField,
      label: $_("Annual leasing fee area"),
      extras: { unit: $_("ha") },
    },
    annual_leasing_fee_comment: {
      displayField: TextField,
      label: $_("Comment on leasing fee"),
    },
    contract_farming: {
      displayField: BooleanField,
      label: $_("Contract farming"),
    },
    on_the_lease_state: {
      displayField: BooleanField,
      label: $_("On leased / purchased"),
    },
    on_the_lease: {
      displayField: JSONLeaseField,
      label: $_("On leased area/farmers/households"),
    },
    off_the_lease_state: {
      displayField: BooleanField,
      label: $_("Not on leased / purchased (out-grower)"),
    },
    off_the_lease: {
      displayField: JSONLeaseField,
      label: $_("Not on leased area/farmers/households (out-grower)"),
    },
    contract_farming_comment: {
      displayField: TextField,
      label: $_("Comment on contract farming"),
    },
    // EMPLOYMENT
    total_jobs_created: {
      displayField: BooleanField,
      label: $_("Jobs created (total)"),
    },
    total_jobs_planned: {
      displayField: DecimalField,
      label: $_("Planned number of jobs (total)"),
    },
    total_jobs_planned_employees: {
      displayField: DecimalField,
      label: $_("Planned employees (total)"),
    },
    total_jobs_planned_daily_workers: {
      displayField: DecimalField,
      label: $_("Planned daily/seasonal workers (total)"),
    },
    total_jobs_current: {
      displayField: JSONJobsField,
      label: $_("Current total number of jobs/employees/ daily/seasonal workers"),
    },
    total_jobs_created_comment: {
      displayField: TextField,
      label: $_("Comment on jobs created (total)"),
    },
    foreign_jobs_created: {
      displayField: BooleanField,
      label: $_("Jobs created (foreign)"),
    },
    foreign_jobs_planned: {
      displayField: DecimalField,
      label: $_("Planned number of jobs (foreign)"),
    },
    foreign_jobs_planned_employees: {
      displayField: DecimalField,
      label: $_("Planned employees (foreign)"),
    },
    foreign_jobs_planned_daily_workers: {
      displayField: DecimalField,
      label: $_("Planned daily/seasonal workers (foreign)"),
    },
    foreign_jobs_current: {
      displayField: JSONJobsField,
      label: $_("Current foreign number of jobs/employees/ daily/seasonal workers"),
    },
    foreign_jobs_created_comment: {
      displayField: TextField,
      label: $_("Comment on jobs created (foreign)"),
    },
    domestic_jobs_created: {
      displayField: BooleanField,
      label: $_("Jobs created (domestic)"),
    },
    domestic_jobs_planned: {
      displayField: DecimalField,
      label: $_("Planned number of jobs (domestic)"),
    },
    domestic_jobs_planned_employees: {
      displayField: DecimalField,
      label: $_("Planned employees (domestic)"),
    },
    domestic_jobs_planned_daily_workers: {
      displayField: DecimalField,
      label: $_("Planned daily/seasonal workers (domestic)"),
    },
    domestic_jobs_current: {
      displayField: JSONJobsField,
      label: $_("Current domestic number of jobs/employees/ daily/seasonal workers"),
    },
    domestic_jobs_created_comment: {
      displayField: TextField,
      label: $_("Comment on jobs created (domestic)"),
    },
    // Investor Info
    operating_company: {
      displayField: InvestorLinkField,
      label: $_("Operating company"),
    },
    involved_actors: {
      displayField: JSONActorsField,
      label: $_("Actors involved in the negotiation / admission process"),
    },
    project_name: {
      displayField: TextField,
      label: $_("Name of investment project"),
    },
    investment_chain_comment: {
      displayField: TextField,
      label: $_("Comment on investment chain"),
    },
    // Local communities
    name_of_community: {
      displayField: TextField,
      label: $_("Name of community"),
      extras: { multiline: true },
    }, // TODO special case, where we are supposed to parse to multiple entries
    name_of_indigenous_people: {
      displayField: TextField,
      label: $_("Name of indigenous people"),
    }, // TODO special case, where we are supposed to parse to multiple entries
    people_affected_comment: {
      displayField: TextField,
      label: $_("Comment on people affected"),
    },
    recognition_status: {
      displayField: ChoicesField,
      label: $_("Recognition status"),
      extras: { choices: $fieldChoices.deal.recognition_status, multipleChoices: true },
    },
    recognition_status_comment: {
      displayField: TextField,
      label: $_("Comment on recognition status"),
    },
    community_consultation: {
      displayField: ChoicesField,
      label: $_("Community consultation"),
      extras: { choices: $fieldChoices.deal.community_consultation },
    },
    community_consultation_comment: {
      displayField: TextField,
      label: $_("Comment on community consultation"),
    },
    community_reaction: {
      displayField: ChoicesField,
      label: $_("Community reaction"),
      extras: { choices: $fieldChoices.deal.community_reaction },
    },
    community_reaction_comment: {
      displayField: TextField,
      label: $_("Comment on community reaction"),
    },
    land_conflicts: {
      displayField: BooleanField,
      label: $_("Presence of land conflicts"),
    },
    land_conflicts_comment: {
      displayField: TextField,
      label: $_("Comment on presence of land conflicts"),
    },
    displacement_of_people: {
      displayField: BooleanField,
      label: $_("Displacement of people"),
    },
    displaced_people: {
      displayField: DecimalField,
      label: $_("Number of people actually displaced"),
    },
    displaced_households: {
      displayField: DecimalField,
      label: $_("Number of households actually displaced"),
    },
    displaced_people_from_community_land: {
      displayField: DecimalField,
      label: $_("Number of people displaced out of their community land"),
    },
    displaced_people_within_community_land: {
      displayField: DecimalField,
      label: $_("Number of people displaced staying on community land"),
    },
    displaced_households_from_fields: {
      displayField: DecimalField,
      label: $_('Number of households displaced "only" from their agricultural fields'),
    },
    displaced_people_on_completion: {
      displayField: DecimalField,
      label: $_(
        "Number of people facing displacement once project is fully implemented",
      ),
    },
    displacement_of_people_comment: {
      displayField: TextField,
      label: $_("Comment on displacement of people"),
    },
    negative_impacts: {
      displayField: ChoicesField,
      label: $_("Negative impacts for local communities"),
      extras: { choices: $fieldChoices.deal.negative_impacts, multipleChoices: true },
    },
    negative_impacts_comment: {
      displayField: TextField,
      label: $_("Comment on negative impacts for local communities"),
    },
    promised_compensation: {
      displayField: TextField,
      label: $_("Promised compensation (e.g. for damages or resettlements)"),
    },
    received_compensation: {
      displayField: TextField,
      label: $_("Received compensation (e.g. for damages or resettlements)"),
    },
    promised_benefits: {
      displayField: ChoicesField,
      label: $_("Promised benefits for local communities"),
      extras: { choices: $fieldChoices.deal.benefits, multipleChoices: true },
    },
    promised_benefits_comment: {
      displayField: TextField,
      label: $_("Comment on promised benefits for local communities"),
    },
    materialized_benefits: {
      displayField: ChoicesField,
      label: $_("Materialized benefits for local communities"),
      extras: { choices: $fieldChoices.deal.benefits, multipleChoices: true },
    },
    materialized_benefits_comment: {
      displayField: TextField,
      label: $_("Comment on materialized benefits for local communities"),
    },
    presence_of_organizations: {
      displayField: TextField,
      label: $_(
        "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
      ),
    },
    // Former Use
    former_land_owner: {
      displayField: ChoicesField,
      label: $_("Former land owner"),
      extras: { choices: $fieldChoices.deal.former_land_owner, multipleChoices: true },
    },
    former_land_owner_comment: {
      displayField: TextField,
      label: $_("Comment on former land owner"),
    },
    former_land_use: {
      displayField: ChoicesField,
      label: $_("Former land use"),
      extras: { choices: $fieldChoices.deal.former_land_use, multipleChoices: true },
    },
    former_land_use_comment: {
      displayField: TextField,
      label: $_("Comment on former land use"),
    },
    former_land_cover: {
      displayField: ChoicesField,
      label: $_("Former land cover"),
      extras: { choices: $fieldChoices.deal.former_land_cover, multipleChoices: true },
    },
    former_land_cover_comment: {
      displayField: TextField,
      label: $_("Comment on former land cover"),
    },
    // // Produce Info
    crops: {
      displayField: JSONExportsField,
      label: $_("Crops area/yield/export"),
      extras: { choices: $fieldChoices.deal.crops },
    },
    crops_comment: { displayField: TextField, label: $_("Comment on crops") },
    animals: {
      displayField: JSONExportsField,
      label: $_("Livestock area/yield/export"),
      extras: { choices: $fieldChoices.deal.animals },
    },
    animals_comment: { displayField: TextField, label: $_("Comment on livestock") },
    mineral_resources: {
      displayField: JSONExportsField,
      label: $_("Mineral resources area/yield/export"),
      extras: { choices: $fieldChoices.deal.minerals },
    },
    mineral_resources_comment: {
      displayField: TextField,
      label: $_("Comment on mineral resources"),
    },
    contract_farming_crops: {
      displayField: JSONCurrentDateAreaChoicesField,
      label: $_("Contract farming crops"),
      extras: { choices: $fieldChoices.deal.crops },
    },
    contract_farming_crops_comment: {
      displayField: TextField,
      label: $_("Comment on contract farming crops"),
    },
    contract_farming_animals: {
      displayField: JSONCurrentDateAreaChoicesField,
      label: $_("Contract farming animals"),
      extras: { choices: $fieldChoices.deal.animals },
    },
    contract_farming_animals_comment: {
      displayField: TextField,
      label: $_("Comment on contract farming animals"),
    },
    electricity_generation: {
      displayField: JSONElectricityGenerationField,
      label: $_("Electricity generation"),
    },
    electricity_generation_comment: {
      displayField: TextField,
      label: $_("Comment on contract farming animals"),
    },
    carbon_sequestration: {
      displayField: JSONCarbonSequestrationField,
      label: $_("Carbon sequestration"),
    },
    carbon_sequestration_comment: {
      displayField: TextField,
      label: $_("Comment on carbon sequestration"),
    },
    has_domestic_use: { displayField: BooleanField, label: $_("Has domestic use") },
    domestic_use: { displayField: DecimalField, label: $_("Domestic use") },
    has_export: { displayField: BooleanField, label: $_("Has export") },
    export: { displayField: DecimalField, label: $_("Export") },
    export_country1: { displayField: CountryField, label: $_("Counrtry 1") },
    export_country1_ratio: {
      displayField: DecimalField,
      label: $_("Counrtry 1 ratio"),
    },
    export_country2: { displayField: CountryField, label: $_("Counrtry 2") },
    export_country2_ratio: {
      displayField: DecimalField,
      label: $_("Counrtry 2 ratio"),
    },
    export_country3: { displayField: CountryField, label: $_("Counrtry 3") },
    export_country3__ratio: {
      displayField: DecimalField,
      label: $_("Counrtry 3 ratio"),
    },
    use_of_produce_comment: {
      displayField: TextField,
      label: $_("Comment on use of produce"),
    },
    in_country_processing: {
      displayField: BooleanField,
      label: $_("In country processing of produce"),
    },
    in_country_processing_comment: {
      displayField: TextField,
      label: $_("Comment on in country processing of produce"),
    },
    in_country_processing_facilities: {
      displayField: TextField,
      label: $_(
        "Processing facilities / production infrastructure of the project (e.g. oil mill, ethanol distillery, biomass power plant etc.)",
      ),
    },
    in_country_end_products: {
      displayField: TextField,
      label: $_("In-country end products of the project"),
    },
    // Water
    water_extraction_envisaged: {
      displayField: BooleanField,
      label: $_("Water extraction envisaged"),
    },
    water_extraction_envisaged_comment: {
      displayField: TextField,
      label: $_("Comment on water extraction envisaged"),
    },
    source_of_water_extraction: {
      displayField: ChoicesField,
      label: $_("Source of water extraction"),
      extras: {
        choices: $fieldChoices.deal.water_source,
        multipleChoices: true,
      },
    },
    source_of_water_extraction_comment: {
      displayField: TextField,
      label: $_("Comment on source of water extraction"),
    },
    how_much_do_investors_pay_comment: {
      displayField: TextField,
      label: $_("Comment on how much do investors pay for water"),
    },
    water_extraction_amount: {
      displayField: DecimalField,
      label: $_("Water extraction amount"),
    },
    water_extraction_amount_comment: {
      displayField: TextField,
      label: $_("Comment on how much water is extracted"),
    },
    use_of_irrigation_infrastructure: {
      displayField: BooleanField,
      label: $_("Use of irrigation infrastructure"),
    },
    use_of_irrigation_infrastructure_comment: {
      displayField: TextField,
      label: $_("Comment on use of irrigation infrastructure"),
    },
    water_footprint: {
      displayField: TextField,
      label: $_("Water footprint of the investment project"),
    },
    // Gender
    gender_related_information: {
      displayField: TextField,
      label: $_("Comment on gender-related info"),
    },
    // Overall comment
    overall_comment: { displayField: TextField, label: $_("Overall comment") },
    // Calc
    deal_size: {
      displayField: DecimalField,
      label: $_("Deal size"),
      extras: { unit: $_("ha") },
    },
    current_negotiation_status: {
      displayField: ChoicesField,
      label: $_("Current negotiation status"),
      extras: { choices: $fieldChoices.deal.negotiation_status },
    },
    current_intention_of_investment: {
      displayField: IOIField,
      label: $_("Intention of investment"),
    },
    current_implementation_status: {
      displayField: ChoicesField,
      label: $_("Current implementation status"),
      extras: { choices: $fieldChoices.deal.implementation_status },
    },
    current_contract_size: {
      displayField: DecimalField,
      label: $_("Current contract size"),
      extras: { unit: $_("ha") },
    },
    //  DATASOURCES
    "location.nid": { displayField: NanoIDField, label: $_("ID") },
    "location.name": { displayField: TextField, label: $_("Location") },
    "location.description": { displayField: TextField, label: $_("Description") },
    "location.facility_name": { displayField: TextField, label: $_("Facility name") },
    "location.comment": { displayField: TextField, label: $_("Comment") },
    "location.point": { displayField: PointField, label: $_("Point") },
    "location.level_of_accuracy": {
      displayField: ChoicesField,
      label: $_("Spatial accuracy level"),
      extras: { choices: $fieldChoices.deal.level_of_accuracy },
    },
    "datasource.nid": { displayField: NanoIDField, label: $_("ID") },
    "datasource.type": {
      displayField: TextField,
      label: $_("Type"),
      extras: { choices: $fieldChoices.datasource.type },
    },
    "datasource.url": {
      displayField: TextField,
      label: $_("URL"),
      extras: { url: true },
    },
    "involvement.relationship": { displayField: TextField, label: $_("Relationship") },
    "involvement.percentage": {
      displayField: DecimalField,
      label: $_("Ownership share"),
      extras: { unit: "%" },
    },
    "involvement.investment_type": {
      displayField: ChoicesField,
      label: $_("Investment type"),
      extras: {
        choices: $fieldChoices.involvement.investment_type,
        multipleChoices: true,
      },
    },
    "involvement.comment": { displayField: TextField, label: $_("Comment") },
  } as { [key: string]: Sec }
})
