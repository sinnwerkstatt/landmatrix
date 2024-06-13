import type { GeoJsonObject } from "geojson"

import type { components } from "$lib/openAPI"
import type { User } from "$lib/types/newtypes"

export type AreaType = "production_area" | "contract_area" | "intended_area"

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

export enum AgricultureIoI {
  BIOFUELS = "BIOFUELS",
  BIOMASS_ENERGY_GENERATION = "BIOMASS_ENERGY_GENERATION",
  FODDER = "FODDER",
  FOOD_CROPS = "FOOD_CROPS",
  LIVESTOCK = "LIVESTOCK",
  NON_FOOD_AGRICULTURE = "NON_FOOD_AGRICULTURE",
  AGRICULTURE_UNSPECIFIED = "AGRICULTURE_UNSPECIFIED",
}

export enum ForestryIoI {
  BIOMASS_ENERGY_PRODUCTION = "BIOMASS_ENERGY_PRODUCTION",
  CARBON = "CARBON",
  FOREST_LOGGING = "FOREST_LOGGING",
  TIMBER_PLANTATION = "TIMBER_PLANTATION",
  FORESTRY_UNSPECIFIED = "FORESTRY_UNSPECIFIED",
}

export enum RenewableEnergyIoI {
  SOLAR_PARK = "SOLAR_PARK",
  WIND_FARM = "WIND_FARM",
  RENEWABLE_ENERGY = "RENEWABLE_ENERGY",
}

export enum OtherIoI {
  CONVERSATION = "CONVERSATION",
  INDUSTRY = "INDUSTRY",
  LAND_SPECULATION = "LAND_SPECULATION",
  MINING = "MINING",
  OIL_GAS_EXTRACTION = "OIL_GAS_EXTRACTION",
  TOURISM = "TOURISM",
  OTHER = "OTHER",
}

export enum IntentionOfInvestmentGroup {
  AGRICULTURE = "AGRICULTURE",
  FORESTRY = "FORESTRY",
  RENEWABLE_ENERGY = "RENEWABLE_ENERGY",
  OTHER = "OTHER",
}
// alias
export const IoIGroup = IntentionOfInvestmentGroup
export type IoIGroup = IntentionOfInvestmentGroup

// grouped IoIs
export const IoIGroups = {
  [IoIGroup.AGRICULTURE]: AgricultureIoI,
  [IoIGroup.FORESTRY]: ForestryIoI,
  [IoIGroup.RENEWABLE_ENERGY]: RenewableEnergyIoI,
  [IoIGroup.OTHER]: OtherIoI,
}

// merge intention of investment enums
// 1. merge objects
export const IntentionOfInvestment = {
  ...AgricultureIoI,
  ...ForestryIoI,
  ...RenewableEnergyIoI,
  ...OtherIoI,
}

// 2. create union type
export type IntentionOfInvestment = keyof typeof IntentionOfInvestment

// create shorthand alias
export const IoI = IntentionOfInvestment
export type IoI = IntentionOfInvestment

export const INTENTION_OF_INVESTMENT_GROUP_MAP: {
  [key in IoI]: IoIGroup
} = {
  // agriculture
  [AgricultureIoI.BIOFUELS]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.BIOMASS_ENERGY_GENERATION]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.FOOD_CROPS]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.FODDER]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.LIVESTOCK]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.NON_FOOD_AGRICULTURE]: IoIGroup.AGRICULTURE,
  [AgricultureIoI.AGRICULTURE_UNSPECIFIED]: IoIGroup.AGRICULTURE,
  // forest
  [ForestryIoI.BIOMASS_ENERGY_PRODUCTION]: IoIGroup.FORESTRY,
  [ForestryIoI.CARBON]: IoIGroup.FORESTRY,
  [ForestryIoI.FOREST_LOGGING]: IoIGroup.FORESTRY,
  [ForestryIoI.TIMBER_PLANTATION]: IoIGroup.FORESTRY,
  [ForestryIoI.FORESTRY_UNSPECIFIED]: IoIGroup.FORESTRY,
  // renewable
  [RenewableEnergyIoI.SOLAR_PARK]: IoIGroup.RENEWABLE_ENERGY,
  [RenewableEnergyIoI.WIND_FARM]: IoIGroup.RENEWABLE_ENERGY,
  [RenewableEnergyIoI.RENEWABLE_ENERGY]: IoIGroup.RENEWABLE_ENERGY,
  // other
  [OtherIoI.CONVERSATION]: IoIGroup.OTHER,
  [OtherIoI.INDUSTRY]: IoIGroup.OTHER,
  [OtherIoI.LAND_SPECULATION]: IoIGroup.OTHER,
  [OtherIoI.MINING]: IoIGroup.OTHER,
  [OtherIoI.OIL_GAS_EXTRACTION]: IoIGroup.OTHER,
  [OtherIoI.TOURISM]: IoIGroup.OTHER,
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

export interface BaseItem {
  date?: string
  current?: boolean
}
export interface NegotiationStatusItem extends BaseItem {
  choice: NegotiationStatus
}
export interface ContractSizeItem extends BaseItem {
  area: number
}

export interface Deal {
  id: number
  // status: Status
  // draft_status: DraftStatus | null
  // versions: ObjVersion[]
  // workflowinfos?: WorkflowInfo[]
  created_at: Date
  created_by?: User
  modified_at: Date
  modified_by?: User
  country?: components["schemas"]["Country"]
  country_id?: number
  current_draft_id?: number
  // locations: Location[]
  // contracts: Contract[]
  // datasources: DataSource[]
  // versions: DealVersion[]
  // workflowinfos?: DealWorkflowInfoOld[]
  negotiation_status?: NegotiationStatusItem[]
  contract_size?: ContractSizeItem[]
  current_intention_of_investment?: IntentionOfInvestment[]
  current_negotiation_status?: NegotiationStatus
  current_implementation_status?: ImplementationStatus
  current_crops?: string[]
  current_animals?: string[]
  current_mineral_resources?: string[]
  current_electricity_generation?: string[]
  current_carbon_sequestration?: string[]
  fully_updated_at?: Date
  fully_updated?: boolean
  // top_investors?: Investor[]
  deal_size?: number
  current_contract_size?: number
  intended_size?: number
  // operating_company?: Investor
  confidential?: boolean
  is_public?: boolean
  geojson?: GeoJsonObject
  [key: string]: unknown
}
