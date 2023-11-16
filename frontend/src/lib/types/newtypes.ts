import type { GeoJsonObject, Point } from "geojson"

import type { Country } from "$lib/types/wagtail"

export enum DealVersion2Status {
  DRAFT = "DRAFT",
  REVIEW = "REVIEW",
  ACTIVATION = "ACTIVATION",
  ACTIVATED = "ACTIVATED",
  //  OLD
  REJECTED = "REJECTED",
  TO_DELETE = "TO_DELETE",
}
export interface DealHull {
  id: number
  country: Country
  active_version_id: number | null
  draft_version_id: number | null
  confidential: boolean
  confidential_comment: string
  deleted: boolean
  deleted_comment: string
  created_at: string
  created_by_id: number
  fully_updated_at: string
  selected_version: DealVersion2
  versions: {
    id: string
    created_at: string
    created_by_id: number
    sent_to_review_at: string
    sent_to_review_by_id: number
    reviewed_at: string
    reviewed_by_id: number
    activated_at: string
    activated_by_id: number
    fully_updated: boolean
    status: DealVersion2Status
  }[]
}

interface DataSource {
  nid: string
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
export interface DealVersion2 extends DealVersionBase {
  is_public: boolean
  has_known_investor: boolean

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
