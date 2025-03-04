import type { Component, Snippet } from "svelte"
import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import {
  datasourceChoices,
  dealChoices,
  investorChoices,
  involvementChoices,
} from "$lib/fieldChoices"

import ArrayTextField from "$components/Fields/Display2/ArrayTextField.svelte"
import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
import ChoicesField from "$components/Fields/Display2/ChoicesField.svelte"
import CountryField from "$components/Fields/Display2/CountryField.svelte"
import CurrencyField from "$components/Fields/Display2/CurrencyField.svelte"
import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
import DealsLengthField from "$components/Fields/Display2/DealsLengthField.svelte"
import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
import DraftVersionStatusField from "$components/Fields/Display2/DraftVersionStatusField.svelte"
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
import PointField from "$components/Fields/Display2/PointField.svelte"
import TextField from "$components/Fields/Display2/TextField.svelte"
import UserField from "$components/Fields/Display2/UserField.svelte"
import WorkflowInfosField from "$components/Fields/Display2/WorkflowInfosField.svelte"
import ArrayTextEditField from "$components/Fields/Edit2/ArrayTextEditField.svelte"
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

//eslint-disable-next-line @typescript-eslint/no-explicit-any
type Any = any

// Todo: Infer extras type on component basis using generic types
type Extras = { [key: string]: unknown } | Any

interface DisplayFieldProps {
  value: Any
  extras?: Extras
}

interface EditFieldProps extends DisplayFieldProps {
  fieldname: string
  children?: Snippet
  onchange?: () => void
}

interface Field {
  displayField: Component<DisplayFieldProps>
  editField?: Component<EditFieldProps>
  label: string
  useQuotation?: boolean
  extras?: Extras
  displayContextHelp?: string
  editContextHelp?: string
}

type FieldLookup = { [key: string]: Field }

export const prefixObjectKeys = <T extends Record<string, unknown>>(
  obj: T,
  prefix: string,
): Record<string, unknown> =>
  Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [`${prefix}.${key}`, value]),
  )

export const commonHullFields = derived(
  [_],
  ([$_]): FieldLookup => ({
    first_created_at: { displayField: DateTimeField, label: $_("Created at") },
    first_created_by_id: { displayField: UserField, label: $_("Created by") },
  }),
)

export const commonVersionFields = derived(
  [_],
  ([$_]): FieldLookup => ({
    created_at: { displayField: DateTimeField, label: $_("Created at") },
    created_by_id: { displayField: UserField, label: $_("Created by") },
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
    activated_at: {
      displayField: DateTimeField,
      label: $_("Activated at"),
    },
    activated_by_id: {
      displayField: UserField,
      label: $_("Activated by"),
    },
    workflowinfos: {
      displayField: WorkflowInfosField,
      label: $_("Logbook"),
    },
    status: {
      displayField: DraftVersionStatusField,
      label: $_("Status"),
    },
  }),
)

export const datasourceFields = derived(
  [_, datasourceChoices],
  ([$_, $datasourceChoices]): FieldLookup => ({
    type: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Type"),
      extras: {
        choices: $datasourceChoices.type,
        required: true,
        otherHint: $_("Please specify in comment field"),
      },
      displayContextHelp: "display:datasources:type",
      editContextHelp: "edit:datasources:type",
    },
    url: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Url"),
      extras: { url: true },
      displayContextHelp: "display:datasources:url",
      editContextHelp: "edit:datasources:url",
    },
    file: {
      displayField: FileField,
      editField: FileEditField,
      label: $_("File"),
      displayContextHelp: "display:datasources:file",
      editContextHelp: "edit:datasources:file",
    },
    file_not_public: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Keep PDF not public"),
      displayContextHelp: "display:datasources:file_not_public",
      editContextHelp: "edit:datasources:file_not_public",
    },
    publication_title: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Publication title"),
      displayContextHelp: "display:datasources:publication_title",
      editContextHelp: "edit:datasources:publication_title",
    },
    date: {
      displayField: TextField,
      editField: DateEditField,
      label: $_("Date"),
      displayContextHelp: "display:datasources:date",
      editContextHelp: "edit:datasources:date",
    },
    name: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name"),
      displayContextHelp: "display:datasources:name",
      editContextHelp: "edit:datasources:name",
    },
    company: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Organisation"),
      displayContextHelp: "display:datasources:company",
      editContextHelp: "edit:datasources:company",
    },
    email: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Email"),
      extras: { email: true },
      displayContextHelp: "display:datasources:email",
      editContextHelp: "edit:datasources:email",
    },
    phone: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Phone"),
      displayContextHelp: "display:datasources:phone",
      editContextHelp: "edit:datasources:phone",
    },
    includes_in_country_verified_information: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Includes in-country-verified information"),
      extras: { nullable: true },
      displayContextHelp:
        "display:datasources:includes_in_country_verified_information",
      editContextHelp: "edit:datasources:includes_in_country_verified_information",
    },
    open_land_contracts_id: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Open Contracting ID"),
      extras: { ocid: true },
      displayContextHelp: "display:datasources:open_land_contracts_id",
      editContextHelp: "edit:datasources:open_land_contracts_id",
    },
    comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on data source"),
      extras: { multiline: true },
    },
  }),
)

export const involvementFields = derived(
  [_, involvementChoices],
  ([$_, $involvementChoices]): FieldLookup => ({
    parent_investor_id: {
      displayField: InvestorLinkField,
      editField: InvestorForeignKey,
      label: $_("Investor"),
      extras: { required: true, creatable: true },
    },
    role: {
      displayField: ChoicesField,
      label: $_("Role"),
      extras: { choices: $involvementChoices.role },
      displayContextHelp: "display:involvement:role",
      editContextHelp: "edit:involvement:role",
    },
    loans_amount: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Loan amount"),
      displayContextHelp: "display:involvement:loans_amount",
      editContextHelp: "edit:involvement:loans_amount",
    },
    loans_date: {
      displayField: TextField,
      editField: DateEditField,
      label: $_("Loan date"),
      displayContextHelp: "display:involvement:loans_date",
      editContextHelp: "edit:involvement:loans_date",
    },
    loans_currency_id: {
      displayField: CurrencyField,
      label: $_("Loan currency"),
      displayContextHelp: "display:involvement:loans_currency_id",
      editContextHelp: "edit:involvement:loans_currency_id",
    },
    relationship: {
      displayField: TextField,
      label: $_("Relationship"),
      displayContextHelp: "display:involvement:relationship",
      editContextHelp: "edit:involvement:relationship",
    },
    percentage: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Ownership share"),
      extras: { unit: "%", range: [0, 100] },
      displayContextHelp: "display:involvement:percentage",
      editContextHelp: "edit:involvement:percentage",
    },
    investment_type: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Investment type"),
      extras: {
        choices: $involvementChoices.investment_type,
        multipleChoices: true,
      },
      displayContextHelp: "display:involvement:investment_type",
      editContextHelp: "edit:involvement:investment_type",
    },
    parent_relation: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Parent relation"),
      extras: {
        choices: $involvementChoices.parent_relation,
        clearable: true,
      },
      displayContextHelp: "display:involvement:parent_relation",
      editContextHelp: "edit:involvement:parent_relation",
    },
    comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment"),
      extras: { multiline: true },
    },
  }),
)

export const locationFields = derived(
  [_, dealChoices],
  ([$_, $dealChoices]): FieldLookup => ({
    name: {
      displayField: TextField,
      editField: LocationGoogleEditField,
      label: $_("Location"),
      displayContextHelp: "display:locations:name",
      editContextHelp: "edit:locations:name",
    },
    description: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Description"),
      extras: { multiline: true },
      displayContextHelp: "display:locations:description",
      editContextHelp: "edit:locations:description",
    },
    point: {
      displayField: PointField,
      editField: PointEditField,
      label: $_("Point"),
      displayContextHelp: "display:locations:point",
      editContextHelp: "edit:locations:point",
    },
    facility_name: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Facility name"),
      displayContextHelp: "display:locations:facility_name",
      editContextHelp: "edit:locations:facility_name",
    },
    level_of_accuracy: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Spatial accuracy level"),
      extras: { choices: $dealChoices.level_of_accuracy },
      displayContextHelp: "display:locations:level_of_accuracy",
      editContextHelp: "edit:locations:level_of_accuracy",
    },
    comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment"),
      extras: { multiline: true },
    },
    // TODO: Add location.areas field components
    // areas: {
    //   displayField: null,
    //   editField: null,
    //   label: $_("Areas"),
    // }
  }),
)

export const contractFields = derived(
  [_],
  ([$_]): FieldLookup => ({
    number: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Contract number"),
      displayContextHelp: "display:contracts:number",
      editContextHelp: "edit:contracts:number",
    },
    date: {
      displayField: TextField,
      editField: DateEditField,
      label: $_("Date"),
      displayContextHelp: "display:contracts:date",
      editContextHelp: "edit:contracts:date",
    },
    expiration_date: {
      displayField: TextField,
      editField: DateEditField,
      label: $_("Expiration date"),
      displayContextHelp: "display:contracts:expiration_date",
      editContextHelp: "edit:contracts:expiration_date",
    },
    agreement_duration: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Duration of the agreement"),
      extras: { unit: $_("years") },
      displayContextHelp: "display:contracts:agreement_duration",
      editContextHelp: "edit:contracts:agreement_duration",
    },
    comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on contract"),
      extras: { multiline: true },
    },
  }),
)

export const investorFields = derived(
  [
    _,
    investorChoices,
    commonHullFields,
    commonVersionFields,
    involvementFields,
    datasourceFields,
  ],
  ([
    $_,
    $investorChoices,
    $commonHullFields,
    $commonVersionFields,
    $involvementFields,
    $datasourceFields,
  ]): FieldLookup => ({
    // Investor Hull
    ...$commonHullFields,
    id: {
      displayField: IDField,
      label: $_("ID"),
      extras: { model: "investor" },
    },

    // Investor Version
    ...$commonVersionFields,
    country: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country of registration/origin"),
      displayContextHelp: "display:investor:country",
      editContextHelp: "edit:investor:country",
    },
    country_id: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country of registration/origin"),
      displayContextHelp: "display:investor:country",
      editContextHelp: "edit:investor:country",
    },
    name: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name"),
      displayContextHelp: "display:investor:name",
      editContextHelp: "edit:investor:name",
    },
    homepage: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Investor homepage"),
      extras: { url: true },
      displayContextHelp: "display:investor:homepage",
      editContextHelp: "edit:investor:homepage",
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
      displayContextHelp: "display:investor:opencorporates",
      editContextHelp: "edit:investor:opencorporates",
    },
    classification: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Classification"),
      extras: { choices: $investorChoices.classification },
      displayContextHelp: "display:investor:classification",
      editContextHelp: "edit:investor:classification",
    },

    // submodels
    ...prefixObjectKeys($involvementFields, "involvement"),
    ...prefixObjectKeys($datasourceFields, "datasource"),

    // derived
    deals: { displayField: DealsLengthField, label: $_("Deals") },
  }),
)

export const dealFields = derived(
  [
    _,
    dealChoices,
    commonHullFields,
    commonVersionFields,
    datasourceFields,
    contractFields,
    locationFields,
  ],
  ([
    $_,
    $dealChoices,
    $commonHullFields,
    $commonVersionFields,
    $datasourceFields,
    $contractFields,
    $locationFields,
  ]): FieldLookup => ({
    // Deal Hull
    ...$commonHullFields,
    id: { displayField: IDField, label: $_("ID") },
    country_id: { displayField: CountryField, label: $_("Target country") },
    confidential: { displayField: BooleanField, label: $_("Confidential") },
    fully_updated: { displayField: BooleanField, label: $_("Fully updated") },
    fully_updated_at: { displayField: DateTimeField, label: $_("Last full update") },

    // Deal Version
    ...$commonVersionFields,

    // General
    intended_size: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Intended size"),
      extras: { unit: $_("ha") },
      useQuotation: true,
      displayContextHelp: "display:intended_size",
      editContextHelp: "edit:intended_size",
    },
    contract_size: {
      displayField: JSONCurrentDateAreaField,
      editField: JSONCurrentDateAreaEditField,
      label: $_("Size under contract (leased or purchased area)"),
      displayContextHelp: "display:contract_size",
      editContextHelp: "edit:contract_size",
    },
    production_size: {
      displayField: JSONCurrentDateAreaField,
      editField: JSONCurrentDateAreaEditField,
      label: $_("Size in operation (production)"),
      displayContextHelp: "display:production_size",
      editContextHelp: "edit:production_size",
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
      extras: { choices: $dealChoices.intention_of_investment },
      displayContextHelp: "display:intention_of_investment",
      editContextHelp: "edit:intention_of_investment",
    },
    intention_of_investment_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on intention of investment"),
      extras: { multiline: true },
    },
    carbon_offset_project: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Carbon offset project"),
      extras: { nullable: true },
      displayContextHelp: "display:carbon_offset_project",
      editContextHelp: "edit:carbon_offset_project",
    },
    carbon_offset_project_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on carbon offset project"),
      extras: { multiline: true },
    },
    nature_of_deal: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Nature of the deal"),
      extras: { choices: $dealChoices.nature_of_deal, multipleChoices: true },
      displayContextHelp: "display:nature_of_deal",
      editContextHelp: "edit:nature_of_deal",
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
      extras: { choices: $dealChoices.negotiation_status },
      displayContextHelp: "display:negotiation_status",
      editContextHelp: "edit:negotiation_status",
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
        choices: $dealChoices.implementation_status,
      },
      displayContextHelp: "display:implementation_status",
      editContextHelp: "edit:implementation_status",
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
      displayContextHelp: "display:purchase_price",
      editContextHelp: "edit:purchase_price",
    },
    // still we need the individual display components for compare view
    purchase_price_currency: {
      displayField: CurrencyField,
      label: $_("Purchase price currency"),
      displayContextHelp: "display:purchase_price_currency",
      editContextHelp: "edit:purchase_price_currency",
    },
    purchase_price_type: {
      displayField: TextField,
      label: $_("Purchase price type"),
      displayContextHelp: "display:purchase_price_type",
      editContextHelp: "edit:purchase_price_type",
    },
    purchase_price_area: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Purchase price area"),
      extras: { unit: $_("ha") },
      displayContextHelp: "display:purchase_price_area",
      editContextHelp: "edit:purchase_price_area",
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
      displayContextHelp: "display:annual_leasing_fee",
      editContextHelp: "edit:annual_leasing_fee",
    },
    // still we need the individual display components for compare view
    annual_leasing_fee_currency: {
      displayField: CurrencyField,
      label: $_("Annual leasing fee currency"),
      displayContextHelp: "display:annual_leasing_fee_currency",
      editContextHelp: "edit:annual_leasing_fee_currency",
    },
    annual_leasing_fee_type: {
      displayField: TextField,
      label: $_("Annual leasing fee type"),
      displayContextHelp: "display:annual_leasing_fee_type",
      editContextHelp: "edit:annual_leasing_fee_type",
    },
    annual_leasing_fee_area: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Annual leasing fee area"),
      extras: { unit: $_("ha") },
      displayContextHelp: "display:annual_leasing_fee_area",
      editContextHelp: "edit:annual_leasing_fee_area",
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
      displayContextHelp: "display:contract_farming",
      editContextHelp: "edit:contract_farming",
    },
    on_the_lease_state: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("On leased / purchased"),
      extras: { nullable: true },
      displayContextHelp: "display:on_the_lease_state",
      editContextHelp: "edit:on_the_lease_state",
    },
    on_the_lease: {
      displayField: JSONLeaseField,
      editField: JSONLeaseEditField,
      label: $_("On leased area/farmers/households"),
      displayContextHelp: "display:on_the_lease",
      editContextHelp: "edit:on_the_lease",
    },
    off_the_lease_state: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Not on leased / purchased (out-grower)"),
      extras: { nullable: true },
      displayContextHelp: "display:off_the_lease_state",
      editContextHelp: "edit:off_the_lease_state",
    },
    off_the_lease: {
      displayField: JSONLeaseField,
      editField: JSONLeaseEditField,
      label: $_("Not on leased area/farmers/households (out-grower)"),
      displayContextHelp: "display:off_the_lease",
      editContextHelp: "edit:off_the_lease",
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
      displayContextHelp: "display:total_jobs_created",
      editContextHelp: "edit:total_jobs_created",
    },
    total_jobs_planned: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned number of jobs (total)"),
      extras: { unit: $_("jobs") },
      displayContextHelp: "display:total_jobs_planned",
      editContextHelp: "edit:total_jobs_planned",
    },
    total_jobs_planned_employees: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned employees (total)"),
      extras: { unit: $_("employees") },
      displayContextHelp: "display:total_jobs_planned_employees",
      editContextHelp: "edit:total_jobs_planned_employees",
    },
    total_jobs_planned_daily_workers: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned daily/seasonal workers (total)"),
      extras: { unit: $_("workers") },
      displayContextHelp: "display:total_jobs_planned_daily_workers",
      editContextHelp: "edit:total_jobs_planned_daily_workers",
    },
    total_jobs_current: {
      displayField: JSONJobsField,
      editField: JSONJobsEditField,
      label: $_("Current total number of jobs/employees/ daily/seasonal workers"),
      displayContextHelp: "display:total_jobs_current",
      editContextHelp: "edit:total_jobs_current",
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
      displayContextHelp: "display:foreign_jobs_created",
      editContextHelp: "edit:foreign_jobs_created",
    },
    foreign_jobs_planned: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned number of jobs (foreign)"),
      extras: { unit: $_("jobs") },
      displayContextHelp: "display:foreign_jobs_planned",
      editContextHelp: "edit:foreign_jobs_planned",
    },
    foreign_jobs_planned_employees: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned employees (foreign)"),
      extras: { unit: $_("employees") },
      displayContextHelp: "display:foreign_jobs_planned_employees",
      editContextHelp: "edit:foreign_jobs_planned_employees",
    },
    foreign_jobs_planned_daily_workers: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned daily/seasonal workers (foreign)"),
      extras: { unit: $_("workers") },
      displayContextHelp: "display:foreign_jobs_planned_daily_workers",
      editContextHelp: "edit:foreign_jobs_planned_daily_workers",
    },
    foreign_jobs_current: {
      displayField: JSONJobsField,
      editField: JSONJobsEditField,
      label: $_("Current foreign number of jobs/employees/ daily/seasonal workers"),
      displayContextHelp: "display:foreign_jobs_current",
      editContextHelp: "edit:foreign_jobs_current",
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
      displayContextHelp: "display:domestic_jobs_created",
      editContextHelp: "edit:domestic_jobs_created",
    },
    domestic_jobs_planned: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned number of jobs (domestic)"),
      extras: { unit: $_("jobs") },
      displayContextHelp: "display:domestic_jobs_planned",
      editContextHelp: "edit:domestic_jobs_planned",
    },
    domestic_jobs_planned_employees: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned employees (domestic)"),
      extras: { unit: $_("employees") },
      displayContextHelp: "display:domestic_jobs_planned_employees",
      editContextHelp: "edit:domestic_jobs_planned_employees",
    },
    domestic_jobs_planned_daily_workers: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Planned daily/seasonal workers (domestic)"),
      extras: { unit: $_("workers") },
      displayContextHelp: "display:domestic_jobs_planned_daily_workers",
      editContextHelp: "edit:domestic_jobs_planned_daily_workers",
    },
    domestic_jobs_current: {
      displayField: JSONJobsField,
      editField: JSONJobsEditField,
      label: $_("Current domestic number of jobs/employees/ daily/seasonal workers"),
      displayContextHelp: "display:domestic_jobs_current",
      editContextHelp: "edit:domestic_jobs_current",
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
      extras: { creatable: true },
      displayContextHelp: "display:operating_company",
      editContextHelp: "edit:operating_company",
    },
    involved_actors: {
      displayField: JSONActorsField,
      editField: JSONActorsEditField,
      label: $_("Actors involved in the negotiation / admission process"),
      displayContextHelp: "display:involved_actors",
      editContextHelp: "edit:involved_actors",
    },
    project_name: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Name of investment project"),
      displayContextHelp: "display:project_name",
      editContextHelp: "edit:project_name",
    },
    investment_chain_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on investment chain"),
      extras: { multiline: true },
    },
    // Local communities
    name_of_community: {
      displayField: ArrayTextField,
      editField: ArrayTextEditField,
      label: $_("Name of community"),
      displayContextHelp: "display:name_of_community",
      editContextHelp: "edit:name_of_community",
    },
    //  see http://localhost:9000/deal/6552/#local_communities as example
    name_of_indigenous_people: {
      displayField: ArrayTextField,
      editField: ArrayTextEditField,
      label: $_("Name of indigenous people"),
      displayContextHelp: "display:name_of_indigenous_people",
      editContextHelp: "edit:name_of_indigenous_people",
    },
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
      extras: { choices: $dealChoices.recognition_status, multipleChoices: true },
      displayContextHelp: "display:recognition_status",
      editContextHelp: "edit:recognition_status",
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
      extras: { choices: $dealChoices.community_consultation, clearable: true },
      displayContextHelp: "display:community_consultation",
      editContextHelp: "edit:community_consultation",
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
      extras: { choices: $dealChoices.community_reaction, clearable: true },
      displayContextHelp: "display:community_reaction",
      editContextHelp: "edit:community_reaction",
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
      displayContextHelp: "display:land_conflicts",
      editContextHelp: "edit:land_conflicts",
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
      displayContextHelp: "display:displacement_of_people",
      editContextHelp: "edit:displacement_of_people",
    },
    displaced_people: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of people actually displaced"),
      displayContextHelp: "display:displaced_people",
      editContextHelp: "edit:displaced_people",
    },
    displaced_households: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of households actually displaced"),
      displayContextHelp: "display:displaced_households",
      editContextHelp: "edit:displaced_households",
    },
    displaced_people_from_community_land: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of people displaced out of their community land"),
      displayContextHelp: "display:displaced_people_from_community_land",
      editContextHelp: "edit:displaced_people_from_community_land",
    },
    displaced_people_within_community_land: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Number of people displaced staying on community land"),
      displayContextHelp: "display:displaced_people_within_community_land",
      editContextHelp: "edit:displaced_people_within_community_land",
    },
    displaced_households_from_fields: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_('Number of households displaced "only" from their agricultural fields'),
      displayContextHelp: "display:displaced_households_from_fields",
      editContextHelp: "edit:displaced_households_from_fields",
    },
    displaced_people_on_completion: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_(
        "Number of people facing displacement once project is fully implemented",
      ),
      displayContextHelp: "display:displaced_people_on_completion",
      editContextHelp: "edit:displaced_people_on_completion",
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
      extras: { choices: $dealChoices.negative_impacts, multipleChoices: true },
      displayContextHelp: "display:negative_impacts",
      editContextHelp: "edit:negative_impacts",
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
      displayContextHelp: "display:promised_compensation",
      editContextHelp: "edit:promised_compensation",
    },
    received_compensation: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Received compensation (e.g. for damages or resettlements)"),
      extras: { multiline: true },
      displayContextHelp: "display:received_compensation",
      editContextHelp: "edit:received_compensation",
    },
    promised_benefits: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Promised benefits for local communities"),
      extras: { choices: $dealChoices.benefits, multipleChoices: true },
      displayContextHelp: "display:promised_benefits",
      editContextHelp: "edit:promised_benefits",
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
      extras: { choices: $dealChoices.benefits, multipleChoices: true },
      displayContextHelp: "display:materialized_benefits",
      editContextHelp: "edit:materialized_benefits",
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
      displayContextHelp: "display:presence_of_organizations",
      editContextHelp: "edit:presence_of_organizations",
    },
    // Former Use
    former_land_owner: {
      displayField: ChoicesField,
      editField: ChoicesEditField,
      label: $_("Former land owner"),
      extras: { choices: $dealChoices.former_land_owner, multipleChoices: true },
      displayContextHelp: "display:former_land_owner",
      editContextHelp: "edit:former_land_owner",
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
      extras: { choices: $dealChoices.former_land_use, multipleChoices: true },
      displayContextHelp: "display:former_land_use",
      editContextHelp: "edit:former_land_use",
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
        choices: $dealChoices.former_land_cover,
        multipleChoices: true,
        otherHint: $_("Other: please specify in comment field"),
      },
      displayContextHelp: "display:former_land_cover",
      editContextHelp: "edit:former_land_cover",
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
      extras: { choices: $dealChoices.crops, multipleChoices: true },
      displayContextHelp: "display:crops",
      editContextHelp: "edit:crops",
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
      extras: { choices: $dealChoices.animals, multipleChoices: true },
      displayContextHelp: "display:animals",
      editContextHelp: "edit:animals",
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
      extras: { choices: $dealChoices.minerals, multipleChoices: true },
      displayContextHelp: "display:mineral_resources",
      editContextHelp: "edit:mineral_resources",
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
      extras: { choices: $dealChoices.crops },
      displayContextHelp: "display:contract_farming_crops",
      editContextHelp: "edit:contract_farming_crops",
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
      extras: { choices: $dealChoices.animals },
      displayContextHelp: "display:contract_farming_animals",
      editContextHelp: "edit:contract_farming_animals",
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
      displayContextHelp: "display:electricity_generation",
      editContextHelp: "edit:electricity_generation",
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
      label: $_("Carbon sequestration/offsetting"),
      displayContextHelp: "display:carbon_sequestration",
      editContextHelp: "edit:carbon_sequestration",
    },
    carbon_sequestration_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on carbon sequestration/offsetting"),
      extras: { multiline: true },
    },
    has_domestic_use: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Has domestic use"),
      extras: { nullable: true },
      displayContextHelp: "display:has_domestic_use",
      editContextHelp: "edit:has_domestic_use",
    },
    domestic_use: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Domestic use"),
      extras: { unit: "%", range: [0, 100] },
      displayContextHelp: "display:domestic_use",
      editContextHelp: "edit:domestic_use",
    },
    has_export: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Has export"),
      extras: { nullable: true },
      displayContextHelp: "display:has_export",
      editContextHelp: "edit:has_export",
    },
    export: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Export"),
      extras: { unit: "%", range: [0, 100] },
      displayContextHelp: "display:export",
      editContextHelp: "edit:export",
    },
    export_country1: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country 1"),
      displayContextHelp: "display:export_country1",
      editContextHelp: "edit:export_country1",
    },
    export_country1_ratio: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Country 1 ratio"),
      extras: { unit: "%", range: [0, 100] },
      displayContextHelp: "display:export_country1_ratio",
      editContextHelp: "edit:export_country1_ratio",
    },
    export_country2: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country 2"),
      displayContextHelp: "display:export_country2",
      editContextHelp: "edit:export_country2",
    },
    export_country2_ratio: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Country 2 ratio"),
      extras: { unit: "%", range: [0, 100] },
      displayContextHelp: "display:export_country2_ratio",
      editContextHelp: "edit:export_country2_ratio",
    },
    export_country3: {
      displayField: CountryField,
      editField: CountryEditField,
      label: $_("Country 3"),
      displayContextHelp: "display:export_country3",
      editContextHelp: "edit:export_country3",
    },
    export_country3_ratio: {
      displayField: DecimalField,
      editField: DecimalEditField,
      label: $_("Country 3 ratio"),
      extras: { unit: "%", range: [0, 100] },
      displayContextHelp: "display:export_country3_ratio",
      editContextHelp: "edit:export_country3_ratio",
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
      displayContextHelp: "display:in_country_processing",
      editContextHelp: "edit:in_country_processing",
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
      displayContextHelp: "display:in_country_processing_facilities",
      editContextHelp: "edit:in_country_processing_facilities",
    },
    in_country_end_products: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("In-country end products of the project"),
      extras: { multiline: true },
      displayContextHelp: "display:in_country_end_products",
      editContextHelp: "edit:in_country_end_products",
    },
    // Water
    water_extraction_envisaged: {
      displayField: BooleanField,
      editField: BooleanEditField,
      label: $_("Water extraction envisaged"),
      extras: { nullable: true },
      displayContextHelp: "display:water_extraction_envisaged",
      editContextHelp: "edit:water_extraction_envisaged",
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
        choices: $dealChoices.water_source,
        multipleChoices: true,
      },
      displayContextHelp: "display:source_of_water_extraction",
      editContextHelp: "edit:source_of_water_extraction",
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
      displayContextHelp: "display:water_extraction_amount",
      editContextHelp: "edit:water_extraction_amount",
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
      displayContextHelp: "display:use_of_irrigation_infrastructure",
      editContextHelp: "edit:use_of_irrigation_infrastructure",
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
      displayContextHelp: "display:water_footprint",
      editContextHelp: "edit:water_footprint",
    },
    // Gender
    gender_related_information: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Comment on gender-related info"),
      extras: { multiline: true },
      displayContextHelp: "display:gender_related_information",
      editContextHelp: "edit:gender_related_information",
    },
    // Overall comment
    overall_comment: {
      displayField: TextField,
      editField: TextEditField,
      label: $_("Overall comment"),
      extras: { multiline: true },
      displayContextHelp: "display:overall_comment",
      editContextHelp: "edit:overall_comment",
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
      extras: { choices: $dealChoices.negotiation_status },
    },
    current_intention_of_investment: {
      displayField: IOIField,
      label: $_("Current intention of investment"),
    },
    current_implementation_status: {
      displayField: ChoicesField,
      label: $_("Current implementation status"),
      extras: { choices: $dealChoices.implementation_status },
    },
    current_contract_size: {
      displayField: DecimalField,
      label: $_("Current contract size"),
      extras: { unit: $_("ha") },
    },

    // submodels
    ...prefixObjectKeys($datasourceFields, "datasource"),
    ...prefixObjectKeys($contractFields, "contract"),
    ...prefixObjectKeys($locationFields, "location"),
  }),
)
