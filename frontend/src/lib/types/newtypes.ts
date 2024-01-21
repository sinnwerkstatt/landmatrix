import type { Feature, MultiPolygon, Point, Polygon } from "geojson"
import type { GeoJSON } from "leaflet"

import type { IntentionOfInvestment } from "$lib/types/deal"

type _oneToNine = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
type _zeroToNine = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
type _YYYY = `19${_zeroToNine}${_zeroToNine}` | `20${_zeroToNine}${_zeroToNine}`
type _MM = `0${_oneToNine}` | `1${0 | 1 | 2}`
type _DD = `${0}${_oneToNine}` | `${1 | 2}${_zeroToNine}` | `3${0 | 1}`
// type DateString = `${YYYY}-${MM}-${DD}`   - we would need DateTime, not just Date
type LooseDateString = `${_YYYY}` | `${_YYYY}-${_MM}` | `${_YYYY}-${_MM}-${_DD}`

export enum Version2Status {
  DRAFT = "DRAFT",
  REVIEW = "REVIEW",
  ACTIVATION = "ACTIVATION",
  ACTIVATED = "ACTIVATED",
  //  OLD
  REJECTED = "REJECTED",
  TO_DELETE = "TO_DELETE",
}

type WFReply = {
  timestamp: string
  user_id: number
  comment: string
}

export interface WorkflowInfoType {
  id: number
  from_user_id: number
  to_user_id: number | null
  status_before: Version2Status | null
  status_after: Version2Status | null
  timestamp: string
  comment: string
  resolved: boolean
  replies: WFReply[]
}

export interface Currency {
  id: number
  code: string
  name: string
  symbol: string
}

interface Hull {
  id: number
  active_version_id: number | null
  draft_version_id: number | null
  deleted: boolean
  deleted_comment: string
  first_created_at: string
  first_created_by_id: number
  versions: BaseVersionMixin[]
  workflowinfos: WorkflowInfoType[]
}

export interface DealHull extends Hull {
  selected_version: DealVersion2
  country_id: number | null
  confidential: boolean
  confidential_comment: string
  fully_updated_at: string | null
}

export interface Involvement {
  id: number
  parent_investor_id: number
  child_investor_id: number
  role: string

  investment_type: string[]
  percentage: number
  loans_amount: number
  loans_currency_id: number | null
  loans_date: LooseDateString
  parent_relation: string | null
  comment: string
  // the following are generated on the fly in the backend
  other_investor: {
    id: number
    selected_version: {
      name: string
      country_id: number | null
      classification: string
    }
    deleted: boolean
  }
  relationship: string
}

export interface InvestorHull extends Hull {
  selected_version: InvestorVersion2

  deals: DealHull[]
  involvements: Involvement[]
  workflowinfos: WorkflowInfoType[]
}

export class DataSource {
  nid: string
  type: string
  url: string
  file: string | null
  file_not_public: boolean
  publication_title: string
  date: LooseDateString | null
  name: string
  company: string
  email: string
  phone: string
  includes_in_country_verified_information: boolean | null
  open_land_contracts_id: string
  comment: string

  constructor(nid: string) {
    this.nid = nid
    this.type = ""
    this.url = ""
    this.file = null
    this.file_not_public = false
    this.publication_title = ""
    this.date = null
    this.name = ""
    this.company = ""
    this.email = ""
    this.phone = ""
    this.includes_in_country_verified_information = null
    this.open_land_contracts_id = ""
    this.comment = ""
  }
}

export class Contract {
  nid: string
  number: string
  date: LooseDateString | null
  expiration_date: LooseDateString | null
  agreement_duration: number | null
  comment: string

  constructor(nid: string) {
    this.nid = nid
    this.number = ""
    this.date = null
    this.expiration_date = null
    this.agreement_duration = null
    this.comment = ""
  }
}

enum ActorRole {
  TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES = "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
  GOVERNMENT_OR_STATE_INSTITUTIONS = "GOVERNMENT_OR_STATE_INSTITUTIONS",
  TRADITIONAL_LOCAL_AUTHORITY = "TRADITIONAL_LOCAL_AUTHORITY",
  BROKER = "BROKER",
  INTERMEDIARY = "INTERMEDIARY",
  OTHER = "OTHER",
}

export interface InvolvedActor {
  name: string
  role: ActorRole
}

interface DealVersionBase {
  id: number

  locations: Location2[]

  intended_size: number | null
  contract_size: JSONCurrentDateAreaFieldType
  production_size: JSONCurrentDateAreaFieldType
  land_area_comment: string

  intention_of_investment: JSONCurrentDateAreaChoicesFieldType
  intention_of_investment_comment: string

  nature_of_deal: string[]
  nature_of_deal_comment: string

  negotiation_status: JSONCurrentDateChoiceFieldType
  negotiation_status_comment: string

  implementation_status: JSONCurrentDateChoiceFieldType
  implementation_status_comment: string

  purchase_price: number | null
  purchase_price_currency: number | null
  purchase_price_type: "PER_HA" | "PER_AREA" | null
  purchase_price_area: number | null
  purchase_price_comment: string

  annual_leasing_fee: number | null
  annual_leasing_fee_currency: number | null
  annual_leasing_fee_type: "PER_HA" | "PER_AREA" | null
  annual_leasing_fee_area: number | null
  annual_leasing_fee_comment: string

  contract_farming: boolean | null
  on_the_lease_state: boolean | null
  on_the_lease: JSONLeaseFieldType
  off_the_lease_state: boolean | null
  off_the_lease: JSONLeaseFieldType
  contract_farming_comment: string

  contracts: Contract[]

  // employment
  total_jobs_created: boolean | null
  total_jobs_planned: number | null
  total_jobs_planned_employees: number | null
  total_jobs_planned_daily_workers: number | null
  total_jobs_current: JSONJobsFieldType
  total_jobs_created_comment: string

  foreign_jobs_created: boolean | null
  foreign_jobs_planned: number | null
  foreign_jobs_planned_employees: number | null
  foreign_jobs_planned_daily_workers: number | null
  foreign_jobs_current: JSONJobsFieldType
  foreign_jobs_created_comment: string

  domestic_jobs_created: boolean | null
  domestic_jobs_planned: number | null
  domestic_jobs_planned_employees: number | null
  domestic_jobs_planned_daily_workers: number | null
  domestic_jobs_current: JSONJobsFieldType
  domestic_jobs_created_comment: string

  operating_company: InvestorHull | null
  operating_company_id: number | null
  involved_actors: InvolvedActor[]
  project_name: string
  investment_chain_comment: string

  name_of_community: []
  name_of_indigenous_people: []
  people_affected_comment: string
  recognition_status: []
  recognition_status_comment: string
  community_consultation: string
  community_consultation_comment: string
  community_reaction: string
  community_reaction_comment: string
  land_conflicts: boolean
  land_conflicts_comment: string
  displacement_of_people: boolean | null
  displaced_people: boolean | null
  displaced_households: number
  displaced_people_from_community_land: number
  displaced_people_within_community_land: number
  displaced_households_from_fields: number
  displaced_people_on_completion: number
  displacement_of_people_comment: string
  negative_impacts: []
  negative_impacts_comment: string
  promised_compensation: string
  received_compensation: string
  promised_benefits: []
  promised_benefits_comment: string
  materialized_benefits: []
  materialized_benefits_comment: string
  presence_of_organizations: string
  former_land_owner: []
  former_land_owner_comment: string
  former_land_use: []
  former_land_use_comment: string
  former_land_cover: []
  former_land_cover_comment: string
  //  produce
  crops: JSONExportsFieldType[]
  crops_comment: string
  animals: JSONExportsFieldType[]
  animals_comment: string
  mineral_resources: JSONExportsFieldType[]
  mineral_resources_comment: string
  contract_farming_crops: JSONCurrentDateAreaChoicesFieldType
  contract_farming_crops_comment: string
  contract_farming_animals: JSONCurrentDateAreaChoicesFieldType
  contract_farming_animals_comment: string
  electricity_generation: JSONElectricityGenerationFieldType
  electricity_generation_comment: string
  carbon_sequestration: JSONCarbonSequestrationFieldType[]
  carbon_sequestration_comment: string
  has_domestic_use: boolean | null
  domestic_use: number | null
  has_export: boolean | null
  export: number | null
  export_country1_id: number | null
  export_country1_ratio: number | null
  export_country2_id: number | null
  export_country2_ratio: number | null
  export_country3_id: number | null
  export_country3_ratio: number | null
  use_of_produce_comment: string
  in_country_processing: boolean | null
  in_country_processing_comment: string
  in_country_processing_facilities: string
  in_country_end_products: string
  // water
  water_extraction_envisaged: boolean
  water_extraction_envisaged_comment: string
  source_of_water_extraction: []
  source_of_water_extraction_comment: string
  how_much_do_investors_pay_comment: string
  water_extraction_amount: number
  water_extraction_amount_comment: string
  use_of_irrigation_infrastructure: boolean
  use_of_irrigation_infrastructure_comment: string
  water_footprint: string

  gender_related_information: string

  overall_comment: string
  datasources: DataSource[]
}

interface BaseVersionMixin {
  id: number
  created_at: string
  created_by_id: number
  modified_at: string | null
  modified_by_id: number | null
  sent_to_review_at: string | null
  sent_to_review_by_id: number | null
  sent_to_activation_at: string | null
  sent_to_activation_by_id: number | null
  activated_at: string | null
  activated_by_id: number | null

  status: Version2Status

  // we have these fields when it's DealVersions
  fully_updated?: boolean
  is_public?: boolean
}

export interface DealVersion2 extends DealVersionBase, BaseVersionMixin {
  fully_updated: boolean
  is_public: boolean
  has_known_investor: boolean

  current_negotiation_status: string
  current_implementation_status: string
  current_intention_of_investment: IntentionOfInvestment[]
  deal_size: number
}

export type JSONCurrentDateAreaFieldType = Array<{
  current: boolean
  date: string | null
  area: number
}>

export type JSONCurrentDateChoiceFieldType = Array<{
  current: boolean
  date: string | null
  choice: string
}>

export type JSONCurrentDateAreaChoicesFieldType = Array<{
  current: boolean
  date: string | null
  area: number | null
  choices: string[]
}>

export type JSONLeaseFieldType = Array<{
  current: boolean
  date: string | null
  area: number | null
  farmers: number | null
  households: number | null
}>

export type JSONJobsFieldType = Array<{
  current: boolean
  date: string | null
  jobs: number | null
  employees: number | null
  workers: number | null
}>

export interface JSONExportsFieldType {
  current: boolean
  date: string | null
  choices: string[]
  area: number | null
  yield: number | null
  export: number | null
}

export interface JSONElectricityGenerationFieldType {
  current: boolean
  date: string | null
  area: number | null
  choices: string[]
  export: number | null
  windfarm_count: number | null
  current_capacity: number | null
  intended_capacity: number | null
}
export interface JSONCarbonSequestrationFieldType {
  current: boolean
  date: string | null
  area: number | null
  choices: string[]
  projected_lifetime_sequestration: number | null
  projected_annual_sequestration: number | null
  certification_standard: boolean | null
  certification_standard_name: string
  certification_standard_comment: string
}

export type AreaType = "production_area" | "contract_area" | "intended_area"

export interface Area {
  id: number
  type: AreaType
  current: boolean
  date: string
  area: Polygon | MultiPolygon // only allowed geometry types, see geojsonValidation.ts
}

export enum ACCURACY_LEVEL {
  COUNTRY,
  ADMINISTRATIVE_REGION,
  APPROXIMATE_LOCATION,
  EXACT_LOCATION,
  COORDINATES,
}

export class Location2 {
  nid: string
  name: string
  description: string
  point: Point | null
  facility_name: string
  level_of_accuracy: ACCURACY_LEVEL | null
  comment: string
  areas: Area[]

  constructor(nid: string) {
    this.nid = nid
    this.name = ""
    this.description = ""
    this.point = null
    this.facility_name = ""
    this.level_of_accuracy = null
    this.comment = ""
    this.areas = []
  }
}

export interface InvestorVersion2 extends BaseVersionMixin {
  name: string
  name_unknown: boolean
  // country: Country | null
  country_id: number | null
  classification: string
  homepage: string
  opencorporates: string
  comment: string
  datasources: DataSource[]
}

// Types for locations + areas in geojson
export interface PointFeatureProps {
  id: string
  level_of_accuracy: ACCURACY_LEVEL | null
  name?: string
}

export type PointFeature = Feature<Point, PointFeatureProps>

export interface AreaFeatureProps {
  id: number
  type: AreaType
  date?: string
  current?: boolean
  visible: boolean
}

export type AreaFeature = Feature<Polygon | MultiPolygon, AreaFeatureProps>
export type AreaFeatureLayer = GeoJSON<AreaFeatureProps, Polygon | MultiPolygon>
