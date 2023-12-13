import type { GeoJsonObject, Point } from "geojson"

import type { Country } from "$lib/types/wagtail"

export enum Version2Status {
  DRAFT = "DRAFT",
  REVIEW = "REVIEW",
  ACTIVATION = "ACTIVATION",
  ACTIVATED = "ACTIVATED",
  //  OLD
  REJECTED = "REJECTED",
  TO_DELETE = "TO_DELETE",
}

export interface Currency {
  id: number
  code: string
  name: string
  symbol: string
}

interface Hull {
  id: number
  // watch out: DRF does not append _id to Foreignkeys, but means _id.
  active_version: number | null
  draft_version: number | null
  deleted: boolean
  deleted_comment: string
  created_at: string
  created_by_id: number
  versions: {
    id: number
    created_at: string
    created_by_id: number
    sent_to_review_at: string
    sent_to_review_by_id: number
    reviewed_at: string
    reviewed_by_id: number
    activated_at: string
    activated_by_id: number
    fully_updated: boolean
    status: Version2Status
  }[]
}
export interface DealHull extends Hull {
  selected_version: DealVersion2
  country: Country
  confidential: boolean
  confidential_comment: string
  fully_updated_at: string
}
export interface InvestorHull extends Hull {
  selected_version: InvestorVersion2
  confidential: never
  confidential_comment: never
  fully_updated_at: never

  involvements: {
    id: number
    other_investor: {
      id: number
      name: string
      country?: Country
      classification: string

      deleted: boolean
    }
    relationship: string
    percentage: number
    investment_type: string
  }[]
}

export class DataSource {
  nid: string
  type: string
  url: string
  file: string | null
  file_not_public: boolean
  publication_title: string
  date: string | null
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
  date: string | null
  expiration_date: string | null
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

  overall_comment: string
  datasources: DataSource[]
}

interface VersionTimestampMixins {
  created_at: string
  created_by_id: number
  modified_at: string
  modified_by_id: number
  sent_to_review_at: string
  sent_to_review_by_id: number
  reviewed_at: string
  reviewed_by_id: number
  activated_at: string
  activated_by_id: number
}
export interface DealVersion2 extends DealVersionBase, VersionTimestampMixins {
  is_public: boolean
  has_known_investor: boolean

  current_negotiation_status: string
  current_implementation_status: string
  deal_size: number
  fully_updated: boolean

  status: Version2Status
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
  area: number
  choices: string[]
}>

export type JSONLeaseFieldType = Array<{
  current: boolean
  date: string | null
  area?: number
  farmers?: number
  households?: number
}>

export type JSONJobsFieldType = Array<{
  current: boolean
  date: string | null
  jobs?: number
  employees?: number
  workers?: number
}>

interface Area {
  id: number
  type: string
  current: boolean
  date: string
  area: GeoJsonObject
}
export class Location2 {
  nid: string
  name: string
  description: string
  point: Point | null
  facility_name: string
  level_of_accuracy: string
  comment: string
  areas: Area[]
  constructor(nid: string) {
    this.nid = nid
    this.name = ""
    this.description = ""
    this.point = null
    this.facility_name = ""
    this.level_of_accuracy = ""
    this.comment = ""
    this.areas = []
  }
}

export interface InvestorVersion2 extends VersionTimestampMixins {
  id: number
  name: string
  name_unknown: boolean
  country: Country
  classification: string
  homepage: string
  opencorporates: string
  comment: string
  datasources: DataSource[]

  status: Version2Status
  deals: DealHull[]
}
