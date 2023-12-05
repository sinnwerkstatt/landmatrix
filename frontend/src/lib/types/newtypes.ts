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

interface DataSource {
  nid: string
  type: string
  url: string
  file: string
  file_not_public: boolean
  publication_title: string
  date: string
  name: string
  company: string
  email: string
  phone: string
  includes_in_country_verified_information: boolean | null
  open_land_contracts_id: string
  comment: string
}

interface DealVersionBase {
  id: number

  locations: Location2[]

  intended_size: number
  contract_size: JSONCurrentDateAreaFieldType
  production_size: JSONCurrentDateAreaFieldType
  land_area_comment: string

  intention_of_investment: JSONCurrentDateAreaChoicesFieldType
  intention_of_investment_comment: string

  nature_of_deal: string[]
  nature_of_deal_comment: string

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

type JSONCurrentDateAreaFieldType = Array<{
  current: boolean
  date: string
  area: number
}>

export type JSONCurrentDateAreaChoicesFieldType = Array<{
  current: boolean
  date: string
  area: number
  choices: string[]
}>

interface Area {
  id: number
  type: string
  current: boolean
  date: string
  area: GeoJsonObject
}
interface Location2 {
  nid: string
  name: string
  description: string
  point: Point
  facility_name: string
  level_of_accuracy: string
  comment: string
  areas: Area[]
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
