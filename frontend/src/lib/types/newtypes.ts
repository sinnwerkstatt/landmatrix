import type { Feature, MultiPolygon, Point, Polygon } from "geojson"
import type { GeoJSON } from "leaflet?client"

import type { components } from "$lib/openAPI"

// helper type to be able to extends components["schemas"] interfaces
// https://stackoverflow.com/questions/78497975
type Named<T> = T

// date helpers
type _oneToNine = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
type _zeroToNine = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
type _YYYY = `19${_zeroToNine}${_zeroToNine}` | `20${_zeroToNine}${_zeroToNine}`
type _MM = `0${_oneToNine}` | `1${0 | 1 | 2}`
type _DD = `${0}${_oneToNine}` | `${1 | 2}${_zeroToNine}` | `3${0 | 1}`
// type DateString = `${YYYY}-${MM}-${DD}`   - we would need DateTime, not just Date
type LooseDateString = `${_YYYY}` | `${_YYYY}-${_MM}` | `${_YYYY}-${_MM}-${_DD}`

// TODO: use components["schemas"]["StatusEnum"]
export enum Version2Status {
  DRAFT = "DRAFT",
  REVIEW = "REVIEW",
  ACTIVATION = "ACTIVATION",
  ACTIVATED = "ACTIVATED",
  //  OLD
  REJECTED = "REJECTED",
  TO_DELETE = "TO_DELETE",
  DELETED = "DELETED",
}

// TODO: Fix type in openAPI -> currently just string
export interface WorkflowInfoType {
  id: number
  from_user_id: number
  to_user_id: number | null
  status_before: Version2Status | null
  status_after: Version2Status | null
  timestamp: string
  comment: string
  resolved: boolean
  replies: {
    timestamp: string
    user_id: number
    comment: string
  }[]
}

export type Currency = components["schemas"]["Currency"]

export interface DealHull extends Omit<components["schemas"]["Deal"], "workflowinfos"> {
  workflowinfos: WorkflowInfoType[]
}

// TODO: Fix type in openAPI -> currently string
export interface Involvement {
  id: number
  parent_investor_id: number
  child_investor_id: number
  role: string

  investment_type: string[]
  percentage: number | null
  loans_amount: number | null
  loans_currency_id: number | null
  loans_date: LooseDateString | null
  parent_relation: string | null
  comment: string
  // the following are generated on the fly in the backend
  other_investor: {
    id: number
    selected_version: {
      name: string
      name_unknown: boolean
      country_id: number | null
      classification: string
    }
    deleted: boolean
  }
  relationship: string
}

export interface InvestorHull
  extends Omit<
    components["schemas"]["Investor"],
    "deals" | "involvements" | "workflowinfos"
  > {
  deals: DealHull[]
  involvements: Involvement[]
  workflowinfos: WorkflowInfoType[]
}

interface DealDataSource extends Named<components["schemas"]["DealDataSource"]> {
  date: LooseDateString | null
}
interface InvestorDataSource
  extends Named<components["schemas"]["InvestorDataSource"]> {
  date: LooseDateString | null
}
export type DataSource = DealDataSource | InvestorDataSource

export interface Contract extends Named<components["schemas"]["Contract"]> {
  date: LooseDateString | null
  expiration_date: LooseDateString | null
}

export type InvolvedActor = components["schemas"]["ActorsItem"]

export type DealVersion2 = components["schemas"]["DealVersion"]

export type JSONCurrentDateAreaFieldType = components["schemas"]["CurrentDateAreaItem"]

export type JSONCurrentDateChoiceFieldType = components["schemas"][
  | "CurrentDateChoiceNegotiationStatusItem"
  | "CurrentDateChoiceImplementationStatusItem"]

export type JSONCurrentDateAreaChoicesFieldType = components["schemas"][
  | "CurrentDateAreaChoicesIOIItem"
  | "CurrentDateAreaChoicesAnimalsItem"
  | "CurrentDateAreaChoicesCropsItem"]

export type JSONLeaseFieldType = components["schemas"]["LeaseItem"]

export type JSONJobsFieldType = components["schemas"]["JobsItem"]

export type JSONExportsFieldType = components["schemas"][
  | "ExportsCropsItem"
  | "ExportsAnimalsItem"
  | "ExportsMineralResourcesItem"]

export type JSONElectricityGenerationFieldType =
  components["schemas"]["ElectricityGenerationItem"]

export type JSONCarbonSequestrationFieldType =
  components["schemas"]["CarbonSequestrationItem"]

export type AreaType = components["schemas"]["LocationAreaTypeEnum"]

export type Area = components["schemas"]["LocationArea"]

export type Location2 = components["schemas"]["Location"]

export type InvestorVersion2 = components["schemas"]["InvestorVersion"]

// Define a ts enum for components["schemas"]["RoleEnum"] for easy access
export enum UserRole {
  ANYBODY = 0,
  REPORTER = 1,
  EDITOR = 2,
  ADMINISTRATOR = 3,
}

export type User = components["schemas"]["User"]

// FRONTEND
// Types for locations + areas in geojson
export interface PointFeatureProps {
  id: string
  level_of_accuracy: Location2["level_of_accuracy"]
  name?: string
}

export type PointFeature = Feature<Point, PointFeatureProps>

export interface AreaFeatureProps {
  id: number
  type: AreaType
  date: string
  current: boolean
  visible: boolean
}

export type AreaFeature = Feature<Polygon | MultiPolygon, AreaFeatureProps>
export type AreaFeatureLayer = GeoJSON<AreaFeatureProps, Polygon | MultiPolygon>
