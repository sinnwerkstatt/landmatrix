import type { components, operations } from "$lib/openAPI"

export type Model = "deal" | "investor"

// helper to mark a readonly model as mutable
export type Mutable<Type> = {
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
}

export interface WFIReply {
  timestamp: string
  user_id: number
  comment: string
}

export type WorkflowInfo = (
  | components["schemas"]["DealWorkflowInfo"]
  | components["schemas"]["InvestorWorkflowInfo"]
) & { replies: WFIReply[] }

export type HaArea = components["schemas"]["HaAreasEnum"]
export type DataSourceType = components["schemas"]["DatasourceTypeEnum"]
export type Currency = components["schemas"]["Currency"]

export type DealHull = components["schemas"]["Deal"]
export type MutableDealHull = Mutable<DealHull>

export enum InvolvementRole {
  PARENT = "PARENT",
  LENDER = "LENDER",
}

export type QuotationItem = components["schemas"]["QuotationItem"]
export type Involvement = components["schemas"]["Involvement"]

export type InvestorDeal = components["schemas"]["InvestorDeal"]

export type InvestorHull = components["schemas"]["Investor"]

export type SearchedInvestor = components["schemas"]["SearchedInvestor"]
export type SimpleInvestor = components["schemas"]["SimpleInvestor"]

export type Country = components["schemas"]["Country"]
export type Region = components["schemas"]["Region"]

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

export type DealQIKey = operations["qi_deal_list"]["parameters"]["query"]["qi"]

export type InvestorQIKey = operations["qi_investor_list"]["parameters"]["query"]["qi"]

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

export type Location2 = components["schemas"]["Location"]

export type InvestorVersion2 = components["schemas"]["InvestorVersion"]

export type IntentionOfInvestment = components["schemas"]["IntentionOfInvestmentEnum"]
export type NegotiationStatus = components["schemas"]["NegotiationStatusEnum"]

export type ImplementationStatus = components["schemas"]["ImplementationStatusEnum"]
export type NatureOfDeal = components["schemas"]["NatureOfDealEnum"]

// Todo: solve differently, get from backend?
// Define a ts enum for IntentionOfInvestment groups
export enum IntentionOfInvestmentGroup {
  AGRICULTURE = "AGRICULTURE",
  FORESTRY = "FORESTRY",
  RENEWABLE_ENERGY = "RENEWABLE_ENERGY",
  OTHER = "OTHER",
}
export type IoIGroupMap = { [key in IntentionOfInvestment]: IntentionOfInvestmentGroup }

export enum NegotiationStatusGroup {
  INTENDED = "INTENDED",
  CONCLUDED = "CONCLUDED",
  FAILED = "FAILED",
  CONTRACT_EXPIRED = "CONTRACT_EXPIRED",
}
export type NegStatGroupMap = { [key in NegotiationStatus]: NegotiationStatusGroup }

export enum ProduceGroup {
  CROPS = "CROPS",
  ANIMALS = "ANIMALS",
  MINERAL_RESOURCES = "MINERAL_RESOURCES",
}

export type Crops = components["schemas"]["CropsEnum"]
export type Animals = components["schemas"]["AnimalsEnum"]
export type Minerals = components["schemas"]["MineralsEnum"]

export type Produce = Crops | Animals | Minerals

// Define a ts enum for components["schemas"]["RoleEnum"] for easy access
export enum UserRole {
  ANYBODY = 0,
  REPORTER = 1,
  EDITOR = 2,
  ADMINISTRATOR = 3,
}

export type User = components["schemas"]["User"]
export type LeanUser = components["schemas"]["LeanUser"]
