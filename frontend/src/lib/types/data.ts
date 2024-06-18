import type { Feature, MultiPolygon, Point, Polygon } from "geojson"
import type { GeoJSON } from "leaflet?client"

import type { components } from "$lib/openAPI"

// helper to mark a readonly model as mutable
type Mutable<Type> = {
  -readonly [Key in keyof Type]: Mutable<Type[Key]>
}

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

export type HaArea = components["schemas"]["HaAreasEnum"]
export type Currency = components["schemas"]["Currency"]

// Fix dealHull type
export interface DealHull extends Omit<components["schemas"]["Deal"], "workflowinfos"> {
  workflowinfos: WorkflowInfoType[]
}

export type MutableDealHull = Mutable<DealHull>

export enum InvolvementRole {
  PARENT = "PARENT",
  LENDER = "LENDER",
}

export type Country = components["schemas"]["Country"]

// TODO: Fix type in openAPI -> currently string
export interface Involvement {
  id: number
  parent_investor_id: number
  child_investor_id: number
  role: InvolvementRole

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

// Fix InvestorHull type
export interface InvestorHull
  extends Omit<
    components["schemas"]["Investor"],
    "deals" | "involvements" | "workflowinfos"
  > {
  deals: DealHull[]
  involvements: Involvement[]
  workflowinfos: WorkflowInfoType[]
}

export type MutableInvestorHull = Mutable<InvestorHull>

export interface DealDataSource extends Named<components["schemas"]["DealDataSource"]> {
  date: LooseDateString | null
}
export interface InvestorDataSource
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

export type NegotiationStatusItem =
  components["schemas"]["CurrentDateChoiceNegotiationStatusItem"]

// Should be equal to components["schemas"]["CurrentIntentionOfInvestmentEnum"]
export type IntentionOfInvestment = components["schemas"]["IntentionOfInvestmentEnum"]
export type NegotiationStatus = components["schemas"]["NegotiationStatusEnum"]

// export const NegotiationStatus: { [key in NegotiationStatus]: key } = {
//   // INTENDED
//   EXPRESSION_OF_INTEREST: "EXPRESSION_OF_INTEREST",
//   UNDER_NEGOTIATION: "UNDER_NEGOTIATION",
//   MEMORANDUM_OF_UNDERSTANDING: "MEMORANDUM_OF_UNDERSTANDING",
//   // CONCLUDED
//   ORAL_AGREEMENT: "ORAL_AGREEMENT",
//   CONTRACT_SIGNED: "CONTRACT_SIGNED",
//   CHANGE_OF_OWNERSHIP: "CHANGE_OF_OWNERSHIP",
//   // FAILED
//   NEGOTIATIONS_FAILED: "NEGOTIATIONS_FAILED",
//   CONTRACT_CANCELED: "CONTRACT_CANCELED",
//   // CONTRACT_EXPIRED
//   CONTRACT_EXPIRED: "CONTRACT_EXPIRED",
// }

export type ImplementationStatus = components["schemas"]["ImplementationStatusEnum"]
export type NatureOfDeal = components["schemas"]["NatureOfDealEnum"]
// export type ProduceGroup = components["schemas"][""]

// Todo: solve differently, get from backend?
// Define a ts enum for IntentionOfInvestment groups
export enum IntentionOfInvestmentGroup {
  AGRICULTURE = "AGRICULTURE",
  FORESTRY = "FORESTRY",
  RENEWABLE_ENERGY = "RENEWABLE_ENERGY",
  OTHER = "OTHER",
}
export enum NegotiationStatusGroup {
  INTENDED = "INTENDED",
  CONCLUDED = "CONCLUDED",
  FAILED = "FAILED",
  CONTRACT_EXPIRED = "CONTRACT_EXPIRED",
}
export enum ProduceGroup {
  CROPS = "CROPS",
  ANIMALS = "ANIMALS",
  MINERAL_RESOURCES = "MINERAL_RESOURCES",
}

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

export type IoIGroupMap = { [key in IntentionOfInvestment]: IntentionOfInvestmentGroup }
export type NegStatGroupMap = { [key in NegotiationStatus]: NegotiationStatusGroup }
