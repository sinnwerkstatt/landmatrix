import type { GeoJsonObject, Feature, FeatureCollection, Geometry } from "geojson"

import type { Obj, ObjVersion, WorkflowInfo } from "$lib/types/generics"
import type { Investor } from "$lib/types/investor"

export enum ACCURACY_LEVEL {
  "",
  COUNTRY,
  ADMINISTRATIVE_REGION,
  APPROXIMATE_LOCATION,
  EXACT_LOCATION,
  COORDINATES,
}

export type AreaType = "production_area" | "contract_area" | "intended_area"

export interface FeatureProps {
  // these are the location id and name -> not unique for feature
  id?: string
  name?: string
  type?: AreaType
  date?: string
  current?: boolean
}

export type AreaFeature = Feature<Geometry, FeatureProps>
export type AreaFeatureCollection = FeatureCollection<Geometry, FeatureProps>

export interface Location {
  id: string
  name?: string
  description?: string
  point?: {
    lat: number
    lng: number
  }
  facility_name?: string
  level_of_accuracy?: ACCURACY_LEVEL
  comment?: string
  areas?: AreaFeatureCollection
}

export interface Contract {
  id: string
}

export interface DataSource {
  id: string
  type: string
  url: string
  file: string
  file_not_public: string
  publication_title: string
  date: string
  name: string
  company: string
  email: string
  phone: string
  includes_in_country_verified_information: string
  open_land_contracts_id: string
  comment: string
  old_group_id: number
}

export enum ProduceGroup {
  CROPS = "CROPS",
  ANIMALS = "ANIMALS",
  MINERAL_RESOURCES = "MINERAL_RESOURCES",
}

export enum NatureOfDeal {
  OUTRIGHT_PURCHASE = "OUTRIGHT_PURCHASE",
  LEASE = "LEASE",
  CONCESSION = "CONCESSION",
  EXPLOITATION_PERMIT = "EXPLOITATION_PERMIT",
  PURE_CONTRACT_FARMING = "PURE_CONTRACT_FARMING",
  OTHER = "OTHER",
}

export enum ImplementationStatus {
  PROJECT_NOT_STARTED = "PROJECT_NOT_STARTED",
  STARTUP_PHASE = "STARTUP_PHASE",
  IN_OPERATION = "IN_OPERATION",
  PROJECT_ABANDONED = "PROJECT_ABANDONED",
}

export enum IntentionOfInvestmentGroup {
  AGRICULTURE = "AGRICULTURE",
  FORESTRY = "FORESTRY",
  OTHER = "OTHER",
}
export const IoIGroup = IntentionOfInvestmentGroup
export type IoIGroup = IntentionOfInvestmentGroup

export enum AgricultureIoI {
  BIOFUELS = "BIOFUELS",
  FOOD_CROPS = "FOOD_CROPS",
  FODDER = "FODDER",
  LIVESTOCK = "LIVESTOCK",
  NON_FOOD_AGRICULTURE = "NON_FOOD_AGRICULTURE",
  AGRICULTURE_UNSPECIFIED = "AGRICULTURE_UNSPECIFIED",
}

export enum ForestryIoI {
  TIMBER_PLANTATION = "TIMBER_PLANTATION",
  FOREST_LOGGING = "FOREST_LOGGING",
  CARBON = "CARBON",
  FORESTRY_UNSPECIFIED = "FORESTRY_UNSPECIFIED",
}

export enum OtherIoI {
  MINING = "MINING",
  OIL_GAS_EXTRACTION = "OIL_GAS_EXTRACTION",
  TOURISM = "TOURISM",
  INDUSTRY = "INDUSTRY",
  CONVERSATION = "CONVERSATION",
  LAND_SPECULATION = "LAND_SPECULATION",
  RENEWABLE_ENERGY = "RENEWABLE_ENERGY",
  OTHER = "OTHER",
}

// merge intention of investment enums
// 1. merge objects
export const IntentionOfInvestment = {
  ...ForestryIoI,
  ...AgricultureIoI,
  ...OtherIoI,
}

// 2. create union type
export type IntentionOfInvestment = keyof typeof IntentionOfInvestment

// create shorthand alias
export const IoI = IntentionOfInvestment
export type IoI = IntentionOfInvestment

export const INTENTION_OF_INVESTMENT_GROUP_MAP: {
  [key in IoI]: IntentionOfInvestmentGroup
} = {
  [AgricultureIoI.BIOFUELS]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.FOOD_CROPS]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.FODDER]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.LIVESTOCK]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.NON_FOOD_AGRICULTURE]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.AGRICULTURE_UNSPECIFIED]: IoIGroup.AGRICULTURE,

  [ForestryIoI.TIMBER_PLANTATION]: IoIGroup.FORESTRY,
  [ForestryIoI.FOREST_LOGGING]: IoIGroup.FORESTRY,
  [ForestryIoI.CARBON]: IoIGroup.FORESTRY,
  [ForestryIoI.FORESTRY_UNSPECIFIED]: IoIGroup.FORESTRY,

  [OtherIoI.MINING]: IoIGroup.OTHER,
  [OtherIoI.OIL_GAS_EXTRACTION]: IoIGroup.OTHER,
  [OtherIoI.TOURISM]: IoIGroup.OTHER,
  [OtherIoI.INDUSTRY]: IoIGroup.OTHER,
  [OtherIoI.CONVERSATION]: IoIGroup.OTHER,
  [OtherIoI.LAND_SPECULATION]: IoIGroup.OTHER,
  [OtherIoI.RENEWABLE_ENERGY]: IoIGroup.OTHER,
  [OtherIoI.OTHER]: IoIGroup.OTHER,
}

export enum NegotiationStatusGroup {
  INTENDED = "INTENDED",
  CONCLUDED = "CONCLUDED",
  FAILED = "FAILED",
  CONTRACT_EXPIRED = "CONTRACT_EXPIRED",
}

export enum NegotiationStatus {
  EXPRESSION_OF_INTEREST = "EXPRESSION_OF_INTEREST",
  UNDER_NEGOTIATION = "UNDER_NEGOTIATION",
  MEMORANDUM_OF_UNDERSTANDING = "MEMORANDUM_OF_UNDERSTANDING",

  ORAL_AGREEMENT = "ORAL_AGREEMENT",
  CONTRACT_SIGNED = "CONTRACT_SIGNED",
  CHANGE_OF_OWNERSHIP = "CHANGE_OF_OWNERSHIP",

  NEGOTIATIONS_FAILED = "NEGOTIATIONS_FAILED",
  CONTRACT_CANCELED = "CONTRACT_CANCELED",

  CONTRACT_EXPIRED = "CONTRACT_EXPIRED",
}

export const NEGOTIATION_STATUS_GROUP_MAP: {
  [key in NegotiationStatus]: NegotiationStatusGroup
} = {
  [NegotiationStatus.EXPRESSION_OF_INTEREST]: NegotiationStatusGroup.INTENDED,
  [NegotiationStatus.UNDER_NEGOTIATION]: NegotiationStatusGroup.INTENDED,
  [NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING]: NegotiationStatusGroup.INTENDED,

  [NegotiationStatus.ORAL_AGREEMENT]: NegotiationStatusGroup.CONCLUDED,
  [NegotiationStatus.CONTRACT_SIGNED]: NegotiationStatusGroup.CONCLUDED,
  [NegotiationStatus.CHANGE_OF_OWNERSHIP]: NegotiationStatusGroup.CONCLUDED,

  [NegotiationStatus.NEGOTIATIONS_FAILED]: NegotiationStatusGroup.FAILED,
  [NegotiationStatus.CONTRACT_CANCELED]: NegotiationStatusGroup.FAILED,

  [NegotiationStatus.CONTRACT_EXPIRED]: NegotiationStatusGroup.CONTRACT_EXPIRED,
}

export interface Deal extends Obj {
  id: number
  locations: Location[]
  contracts: Contract[]
  datasources: DataSource[]
  versions: DealVersion[]
  workflowinfos?: DealWorkflowInfo[]
  current_intention_of_investment?: IntentionOfInvestment[]
  current_negotiation_status?: NegotiationStatus
  current_implementation_status?: ImplementationStatus
  current_crops?: string[]
  current_animals?: string[]
  current_mineral_resources?: string[]
  fully_updated_at?: Date
  fully_updated?: boolean
  top_investors?: Investor[]
  deal_size?: number
  current_contract_size?: number
  intended_size?: number
  operating_company?: Investor
  confidential?: boolean
  is_public?: boolean
  geojson?: GeoJsonObject
  [key: string]: unknown
}

export interface DealVersion extends ObjVersion {
  deal: Deal
}

export interface DealWorkflowInfo extends WorkflowInfo {
  deal: Deal
  deal_version_id: number
}
//
// interface DealAggregation {
//   value: string;
//   count: number;
//   size: number;
// }
// interface DealAggregations {
//   [key: string]: DealAggregation[];
// }
