import type { ComponentType } from "svelte"
import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import { fieldChoices } from "$lib/stores"

import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
import ChoicesField from "$components/Fields/Display2/ChoicesField.svelte"
import CountryField from "$components/Fields/Display2/CountryField.svelte"
import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
import DealsLengthField from "$components/Fields/Display2/DealsLengthField.svelte"
import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
import FileField from "$components/Fields/Display2/FileField.svelte"
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
import WorkflowInfosField from "$components/Fields/Display2/WorkflowInfosField.svelte"
import BooleanEditField from "$components/Fields/Edit2/BooleanEditField.svelte"
import ChoicesEditField from "$components/Fields/Edit2/ChoicesEditField.svelte"
import CountryEditField from "$components/Fields/Edit2/CountryEditField.svelte"
import DateEditField from "$components/Fields/Edit2/DateEditField.svelte"
import DecimalEditField from "$components/Fields/Edit2/DecimalEditField.svelte"
import FileEditField from "$components/Fields/Edit2/FileEditField.svelte"
import InvestorForeignKey from "$components/Fields/Edit2/InvestorForeignKey.svelte"
import JSONActorsEditField from "$components/Fields/Edit2/JSONActorsEditField.svelte"
import JSONCarbonSequestrationEditField from "$components/Fields/Edit2/JSONCarbonSequestrationEditField.svelte"
import JSONCurrentDateAreaChoicesEditField from "$components/Fields/Edit2/JSONCurrentDateAreaChoicesEditField.svelte"
import JSONCurrentDateAreaEditField from "$components/Fields/Edit2/JSONCurrentDateAreaEditField.svelte"
import JSONCurrentDateChoiceEditField from "$components/Fields/Edit2/JSONCurrentDateChoiceEditField.svelte"
import JSONElectricityGenerationEditField from "$components/Fields/Edit2/JSONElectricityGenerationEditField.svelte"
import JSONExportsEditField from "$components/Fields/Edit2/JSONExportsEditField.svelte"
import JSONJobsEditField from "$components/Fields/Edit2/JSONJobsEditField.svelte"
import JSONLeaseEditField from "$components/Fields/Edit2/JSONLeaseEditField.svelte"
import LocationGoogleEditField from "$components/Fields/Edit2/LocationGoogleEditField.svelte"
import PointEditField from "$components/Fields/Edit2/PointEditField.svelte"
import TextEditField from "$components/Fields/Edit2/TextEditField.svelte"

interface Field {
  displayField: ComponentType
  editField?: ComponentType
  label: string
  extras?: unknown
}

export const investorFields = derived([_, fieldChoices], ([$_, $fieldChoices]) => {
  return {
    id: { displayField: IDField, label: $_("ID"), extras: { model: "investor" } },
    country_id: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country of registration/origin"),
      extras: { required: true },
    },
    name: { displayField: TextField, editField: TextEditField, label: $_("Name") },
    homepage: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Investor homepage"),
      extras: { url: true },
    },
    comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment"),
      extras: { multiline: true },
    },
    opencorporates: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Opencorporates link"),
    },
    classification: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Classification"),
      extras: { choices: $fieldChoices.investor.classification },
    },
    //  TODO deduplicate with below's Deal-stuff
    first_created_at: { displayField: DateTimeField, label: $_("Created at") },
    first_created_by_id: { displayField: UserField, label: $_("Created by") },
    created_at: { displayField: DateTimeField, label: $_("Created at") },
    modified_at: { displayField: DateTimeField, label: $_("Last update") },
    workflowinfos: {
      displayField: WorkflowInfosField,
      label: $_("Comments / History"),
    },
    mode: { displayField: TextField, label: $_("Mode") },
    deals: { displayField: DealsLengthField, label: $_("Deals") },
  } as { [key: string]: Field }
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
    displacement_of_people: {
      title: $_("Displacement of people"),
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
    "investor.general_info": {
      title: $_("General info"),
      fields: ["country_id", "classification", "homepage", "opencorporates", "comment"],
    },
  } as { [key: string]: { title: string; fields: string[] } }
})

export const dealFields = derived([_, fieldChoices], ([$_, $fieldChoices]) => {
  return {
    // // Deal Hull
    id: { displayField: IDField, label: $_("ID") },
    country_id: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Target country"),
    },
    confidential: { displayField: BooleanField, label: $_("Confidential") },
    created_at: { displayField: DateTimeField, label: $_("Created at") },
    first_created_at: { displayField: DateTimeField, label: $_("Created at") },
    created_by_id: { displayField: UserField, label: $_("Created by") },
    first_created_by_id: { displayField: UserField, label: $_("Created by") },
    modified_at: { displayField: DateTimeField, label: $_("Last update") },
    modified_by_id: { displayField: UserField, label: $_("Modified by") },
    sent_to_review_at: { displayField: DateTimeField, label: $_("Sent to review at") },
    sent_to_review_by_id: { displayField: UserField, label: $_("Sent to review by") },
    sent_to_activation_at: {
      displayField: DateTimeField,
      label: $_("Sent to activation at"),
    },
    sent_to_activation_by_id: {
      displayField: UserField,
      label: $_("Sent to activation by"),
    },
    activated_at: { displayField: DateTimeField, label: $_("Activated at") },
    activated_by_id: { displayField: UserField, label: $_("Activated by") },

    fully_updated_at: { displayField: DateTimeField, label: $_("Last full update") },
    workflowinfos: {
      displayField: WorkflowInfosField,
      label: $_("Comments / History"),
    },
    mode: { displayField: TextField, label: $_("Mode") },
    // General
    intended_size: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Intended size"),
      extras: { unit: $_("ha") },
    },
    contract_size: {
      displayField: JSONCurrentDateAreaField,
      editField: JSONCurrentDateAreaEditField,
      label: $_("Size under contract (leased or purchased area)"),
    },
    production_size: {
      displayField: JSONCurrentDateAreaField,
      editField: JSONCurrentDateAreaEditField,
      label: $_("Size in operation (production)"),
    },
    land_area_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on land area"),
      extras: { multiline: true },
    },
    intention_of_investment: {
      displayField: JSONCurrentDateAreaChoicesField,
      editField: JSONCurrentDateAreaChoicesEditField,
      label: $_("Intention of investment"),
      extras: { choices: $fieldChoices.deal.intention_of_investment },
    },
    intention_of_investment_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on intention of investment"),
      extras: { multiline: true },
    },
    nature_of_deal: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Nature of the deal"),
      extras: { choices: $fieldChoices.deal.nature_of_deal, multipleChoices: true },
    },
    nature_of_deal_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on nature of the deal"),
      extras: { multiline: true },
    },
    negotiation_status: {
      displayField: JSONCurrentDateChoiceField,
      editField: JSONCurrentDateChoiceEditField,
      label: $_("Negotiation status"),
      extras: { choices: $fieldChoices.deal.negotiation_status },
    },
    negotiation_status_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on negotiation status"),
      extras: { multiline: true },
    },
    implementation_status: {
      displayField: JSONCurrentDateChoiceField,
      editField: JSONCurrentDateChoiceEditField,
      label: $_("Implementation status"),
      extras: {
        choices: $fieldChoices.deal.implementation_status,
      },
    },
    implementation_status_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on implementation status"),
      extras: { multiline: true },
    },
    purchase_price: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Purchase price"),
      extras: { placeholder: "Amount" },
      // we use purchase_price_currency and purchase_price_type here too
    },
    purchase_price_area: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Purchase price area"),
      extras: { unit: $_("ha") },
    },
    purchase_price_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on purchase price"),
      extras: { multiline: true },
    },
    annual_leasing_fee: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Annual leasing fee"),
      extras: { placeholder: "Amount" },
      // we use annual_leasing_fee_currency and ~_type here too
    },
    annual_leasing_fee_area: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Annual leasing fee area"),
      extras: { unit: $_("ha") },
    },
    annual_leasing_fee_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on leasing fee"),
      extras: { multiline: true },
    },
    contract_farming: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Contract farming"),
      extras: { nullable: true },
    },
    on_the_lease_state: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("On leased / purchased"),
      extras: { nullable: true },
    },
    on_the_lease: {
      displayField: JSONLeaseField,
      editField: JSONLeaseEditField,
      label: $_("On leased area/farmers/households"),
    },
    off_the_lease_state: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Not on leased / purchased (out-grower)"),
      extras: { nullable: true },
    },
    off_the_lease: {
      displayField: JSONLeaseField,
      editField: JSONLeaseEditField,
      label: $_("Not on leased area/farmers/households (out-grower)"),
    },
    contract_farming_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on contract farming"),
      extras: { multiline: true },
    },
    // EMPLOYMENT
    total_jobs_created: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Jobs created (total)"),
      extras: { nullable: true },
    },
    total_jobs_planned: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned number of jobs (total)"),
      extras: { unit: $_("jobs") },
    },
    total_jobs_planned_employees: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned employees (total)"),
      extras: { unit: $_("employees") },
    },
    total_jobs_planned_daily_workers: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned daily/seasonal workers (total)"),
      extras: { unit: $_("workers") },
    },
    total_jobs_current: {
      displayField: JSONJobsField,
      editField: JSONJobsEditField,
      label: $_("Current total number of jobs/employees/ daily/seasonal workers"),
    },
    total_jobs_created_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on jobs created (total)"),
      extras: { multiline: true },
    },
    foreign_jobs_created: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Jobs created (foreign)"),
      extras: { nullable: true },
    },
    foreign_jobs_planned: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned number of jobs (foreign)"),
      extras: { unit: $_("jobs") },
    },
    foreign_jobs_planned_employees: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned employees (foreign)"),
      extras: { unit: $_("employees") },
    },
    foreign_jobs_planned_daily_workers: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned daily/seasonal workers (foreign)"),
      extras: { unit: $_("workers") },
    },
    foreign_jobs_current: {
      displayField: JSONJobsField,
      editField: JSONJobsEditField,
      label: $_("Current foreign number of jobs/employees/ daily/seasonal workers"),
    },
    foreign_jobs_created_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on jobs created (foreign)"),
      extras: { multiline: true },
    },
    domestic_jobs_created: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Jobs created (domestic)"),
      extras: { nullable: true },
    },
    domestic_jobs_planned: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned number of jobs (domestic)"),
      extras: { unit: $_("jobs") },
    },
    domestic_jobs_planned_employees: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned employees (domestic)"),
      extras: { unit: $_("employees") },
    },
    domestic_jobs_planned_daily_workers: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned daily/seasonal workers (domestic)"),
      extras: { unit: $_("workers") },
    },
    domestic_jobs_current: {
      displayField: JSONJobsField,
      editField: JSONJobsEditField,
      label: $_("Current domestic number of jobs/employees/ daily/seasonal workers"),
    },
    domestic_jobs_created_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on jobs created (domestic)"),
      extras: { multiline: true },
    },
    // Investor Info
    operating_company: {
      displayField: InvestorLinkField,
      editField: InvestorForeignKey,
      label: $_("Operating company"),
    },
    involved_actors: {
      displayField: JSONActorsField,
      editField: JSONActorsEditField,
      label: $_("Actors involved in the negotiation / admission process"),
    },
    project_name: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name of investment project"),
    },
    investment_chain_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on investment chain"),
      extras: { multiline: true },
    },
    // Local communities
    name_of_community: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name of community"),
      extras: { multiline: true },
    }, // TODO special case, where we are supposed to parse to multiple entries
    //  see http://localhost:9000/deal/6552/#local_communities as example
    name_of_indigenous_people: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name of indigenous people"),
      extras: { multiline: true },
    }, // TODO special case, where we are supposed to parse to multiple entries
    people_affected_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on communities / indigenous peoples affected"),
      extras: { multiline: true },
    },
    recognition_status: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Recognition status of community land tenure"),
      extras: { choices: $fieldChoices.deal.recognition_status, multipleChoices: true },
    },
    recognition_status_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on recognition status of community land tenure"),
      extras: { multiline: true },
    },
    community_consultation: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Community consultation"),
      extras: { choices: $fieldChoices.deal.community_consultation, clearable: true },
    },
    community_consultation_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on consultation of local community"),
      extras: { multiline: true },
    },
    community_reaction: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Community reaction"),
      extras: { choices: $fieldChoices.deal.community_reaction, clearable: true },
    },
    community_reaction_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on community reaction"),
      extras: { multiline: true },
    },
    land_conflicts: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Presence of land conflicts"),
      extras: { nullable: true },
    },
    land_conflicts_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on presence of land conflicts"),
      extras: { multiline: true },
    },
    displacement_of_people: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Displacement of people"),
      extras: { nullable: true },
    },
    displaced_people: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of people actually displaced"),
    },
    displaced_households: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of households actually displaced"),
    },
    displaced_people_from_community_land: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of people displaced out of their community land"),
    },
    displaced_people_within_community_land: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of people displaced staying on community land"),
    },
    displaced_households_from_fields: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_('Number of households displaced "only" from their agricultural fields'),
    },
    displaced_people_on_completion: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_(
        "Number of people facing displacement once project is fully implemented",
      ),
    },
    displacement_of_people_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on displacement of people"),
      extras: { multiline: true },
    },
    negative_impacts: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Negative impacts for local communities"),
      extras: { choices: $fieldChoices.deal.negative_impacts, multipleChoices: true },
    },
    negative_impacts_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on negative impacts for local communities"),
      extras: { multiline: true },
    },
    promised_compensation: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Promised compensation (e.g. for damages or resettlements)"),
      extras: { multiline: true },
    },
    received_compensation: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Received compensation (e.g. for damages or resettlements)"),
      extras: { multiline: true },
    },
    promised_benefits: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Promised benefits for local communities"),
      extras: { choices: $fieldChoices.deal.benefits, multipleChoices: true },
    },
    promised_benefits_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on promised benefits for local communities"),
      extras: { multiline: true },
    },
    materialized_benefits: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Materialized benefits for local communities"),
      extras: { choices: $fieldChoices.deal.benefits, multipleChoices: true },
    },
    materialized_benefits_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on materialized benefits for local communities"),
      extras: { multiline: true },
    },
    presence_of_organizations: {
      displayField: TextField,
      editField: TextEditField,
      label: $_(
        "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
      ),
      extras: { multiline: true },
    },
    // Former Use
    former_land_owner: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Former land owner"),
      extras: { choices: $fieldChoices.deal.former_land_owner, multipleChoices: true },
    },
    former_land_owner_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on former land owner"),
      extras: { multiline: true },
    },
    former_land_use: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Former land use"),
      extras: { choices: $fieldChoices.deal.former_land_use, multipleChoices: true },
    },
    former_land_use_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on former land use"),
      extras: { multiline: true },
    },
    former_land_cover: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Former land cover"),
      extras: {
        choices: $fieldChoices.deal.former_land_cover,
        multipleChoices: true,
        otherHint: $_("Please specify in comment field"),
      },
    },
    former_land_cover_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on former land cover"),
      extras: { multiline: true },
    },
    // // Produce Info
    crops: {
      displayField: JSONExportsField,
      editField: JSONExportsEditField,
      label: $_("Crops area/yield/export"),
      extras: { choices: $fieldChoices.deal.crops, multipleChoices: true },
    },
    crops_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on crops"),
      extras: { multiline: true },
    },
    animals: {
      displayField: JSONExportsField,
      editField: JSONExportsEditField,
      label: $_("Livestock area/yield/export"),
      extras: { choices: $fieldChoices.deal.animals, multipleChoices: true },
    },
    animals_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on livestock"),
      extras: { multiline: true },
    },
    mineral_resources: {
      displayField: JSONExportsField,
      editField: JSONExportsEditField,
      label: $_("Mineral resources area/yield/export"),
      extras: { choices: $fieldChoices.deal.minerals, multipleChoices: true },
    },
    mineral_resources_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on mineral resources"),
      extras: { multiline: true },
    },
    contract_farming_crops: {
      displayField: JSONCurrentDateAreaChoicesField,
      editField: JSONCurrentDateAreaChoicesEditField,
      label: $_("Contract farming crops"),
      extras: { choices: $fieldChoices.deal.crops },
    },
    contract_farming_crops_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on contract farming crops"),
      extras: { multiline: true },
    },
    contract_farming_animals: {
      displayField: JSONCurrentDateAreaChoicesField,
      editField: JSONCurrentDateAreaChoicesEditField,
      label: $_("Contract farming livestock"),
      extras: { choices: $fieldChoices.deal.animals },
    },
    contract_farming_animals_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on contract farming livestock"),
      extras: { multiline: true },
    },
    electricity_generation: {
      displayField: JSONElectricityGenerationField,
      editField: JSONElectricityGenerationEditField,
      label: $_("Electricity generation"),
    },
    electricity_generation_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on electricity generation"),
      extras: { multiline: true },
    },
    carbon_sequestration: {
      displayField: JSONCarbonSequestrationField,
      editField: JSONCarbonSequestrationEditField,
      label: $_("Carbon sequestration"),
    },
    carbon_sequestration_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on carbon sequestration"),
      extras: { multiline: true },
    },
    has_domestic_use: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Has domestic use"),
      extras: { nullable: true },
    },
    domestic_use: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Domestic use"),
      extras: { unit: "%", range: [0, 100] },
    },
    has_export: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Has export"),
      extras: { nullable: true },
    },
    export: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Export"),
      extras: { unit: "%", range: [0, 100] },
    },
    export_country1: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country 1"),
    },
    export_country1_ratio: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Country 1 ratio"),
      extras: { unit: "%", range: [0, 100] },
    },
    export_country2: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country 2"),
    },
    export_country2_ratio: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Country 2 ratio"),
      extras: { unit: "%", range: [0, 100] },
    },
    export_country3: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country 3"),
    },
    export_country3_ratio: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Country 3 ratio"),
      extras: { unit: "%", range: [0, 100] },
    },
    use_of_produce_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on use of produce"),
      extras: { multiline: true },
    },
    in_country_processing: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("In country processing of produce"),
      extras: { nullable: true },
    },
    in_country_processing_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on in country processing of produce"),
      extras: { multiline: true },
    },
    in_country_processing_facilities: {
      displayField: TextField,
      editField: TextEditField,
      label: $_(
        "Processing facilities / production infrastructure of the project (e.g. oil mill, ethanol distillery, biomass power plant etc.)",
      ),
      extras: { multiline: true },
    },
    in_country_end_products: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("In-country end products of the project"),
      extras: { multiline: true },
    },
    // Water
    water_extraction_envisaged: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Water extraction envisaged"),
      extras: { nullable: true },
    },
    water_extraction_envisaged_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on water extraction envisaged"),
      extras: { multiline: true },
    },
    source_of_water_extraction: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Source of water extraction"),
      extras: {
        choices: $fieldChoices.deal.water_source,
        multipleChoices: true,
      },
    },
    source_of_water_extraction_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on source of water extraction"),
      extras: { multiline: true },
    },
    how_much_do_investors_pay_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on how much do investors pay for water"),
      extras: { multiline: true },
    },
    water_extraction_amount: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Water extraction amount"),
      extras: { unit: $_("m3/year") },
    },
    water_extraction_amount_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on how much water is extracted"),
      extras: { multiline: true },
    },
    use_of_irrigation_infrastructure: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Use of irrigation infrastructure"),
      extras: { nullable: true },
    },
    use_of_irrigation_infrastructure_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on use of irrigation infrastructure"),
      extras: { multiline: true },
    },
    water_footprint: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Water footprint of the investment project"),
      extras: { multiline: true },
    },
    // Gender
    gender_related_information: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on gender-related info"),
      extras: { multiline: true },
    },
    // Overall comment
    overall_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Overall comment"),
      extras: { multiline: true },
    },
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
    // LOCATIONS
    "location.nid": { displayField: NanoIDField, label: $_("ID") },
    "location.name": {
      displayField: TextField,
      editField: LocationGoogleEditField,
      label: $_("Location"),
    },
    "location.description": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Description"),
      extras: { multiline: true },
    },
    "location.point": {
      displayField: PointField,
      editField: PointEditField,
      label: $_("Point"),
    },
    "location.facility_name": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Facility name"),
    },
    "location.level_of_accuracy": {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Spatial accuracy level"),
      extras: { choices: $fieldChoices.deal.level_of_accuracy },
    },
    "location.comment": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment"),
      extras: { multiline: true },
    },
    // "location.areas": { displayField: XXX, label: $_("Areas") },
    // CONTRACTS
    "contract.nid": { displayField: NanoIDField, label: $_("ID") },
    "contract.number": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Contract number"),
    },
    "contract.date": {
      displayField: TextField,
      editField: DateEditField,
      label: $_("Date"),
    }, // use DateTimeField TODO? it's loosedatefield
    "contract.expiration_date": {
      displayField: TextField,
      editField: DateEditField,
      label: $_("Expiration date"),
    },
    "contract.agreement_duration": {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Duration of the agreement"),
      extras: { unit: $_("years") },
    },
    "contract.comment": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on contract"),
      extras: { multiline: true },
    },
    // DATASOURCES
    "datasource.nid": { displayField: NanoIDField, label: $_("ID") },
    "datasource.type": {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Type"),
      extras: {
        choices: $fieldChoices.datasource.type,
        otherHint: $_("Please specify in comment field"),
      },
    },
    "datasource.url": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Url"),
      extras: { url: true },
    },
    "datasource.file": {
      displayField: FileField,
      editField: FileEditField,
      label: $_("File"),
    },
    "datasource.file_not_public": {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Keep PDF not public"),
    },
    "datasource.publication_title": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Publication title"),
    },
    "datasource.date": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Date"),
    },
    "datasource.name": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name"),
    },
    "datasource.company": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Organisation"),
    },
    "datasource.email": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Email"),
      extras: { email: true },
    },
    "datasource.phone": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Phone"),
    },
    "datasource.includes_in_country_verified_information": {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Includes in-country-verified information"),
      extras: { nullable: true },
    },
    "datasource.open_land_contracts_id": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Open Contracting ID"),
      extras: { ocid: true },
    },
    "datasource.comment": {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on data source"),
      extras: { multiline: true },
    },
    // INVOLVEMENTS
    //         "involvement_type": {"class": "TextField", "label": _("Involvement type")},
    //         "investor": {"class": "InvestorForeignKey"},
    //         "venture": {"class": "InvestorForeignKey"},
    //         "loans_date": {"class": "DateField"},
    //         "loans_currency": {"class": "CurrencyForeignKey"},
    "involvement.relationship": { displayField: TextField, label: $_("Relationship") },
    "involvement.percentage": {
      displayField: DecimalField,
      label: $_("Ownership share"),
      extras: { unit: "%", range: [0, 100] },
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
  } as { [key: string]: Field }
})
