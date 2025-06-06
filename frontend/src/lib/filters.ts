import { derived, writable } from "svelte/store"

import { browser } from "$app/environment"

import {
  ProduceGroup,
  type ImplementationStatus,
  type IntentionOfInvestment,
  type NatureOfDeal,
  type NegotiationStatus,
} from "$lib/types/data"

export interface ProduceFilter {
  // id: string
  value: string
  label: string
  groupId: ProduceGroup
  group: string
}

export class FilterValues {
  region_id?: number
  country_id?: number
  deal_size_min?: number
  deal_size_max?: number
  negotiation_status: NegotiationStatus[] = []
  nature_of_deal: NatureOfDeal[] = []
  investor_id?: number
  investor_country_id?: number
  initiation_year_min?: number
  initiation_year_max?: number
  initiation_year_unknown = true
  implementation_status: ImplementationStatus[] = []
  intention_of_investment: IntentionOfInvestment[] = []
  produce?: ProduceFilter[] = []
  transnational: boolean | null = null
  forest_concession: boolean | null = null
  carbon_offset_project: boolean | null = null
  produce_info_carbon_offsetting: boolean | null = null

  constructor(data: Partial<FilterValues> = {}) {
    Object.assign(this, data)
  }

  public empty() {
    this.deal_size_min = undefined
    this.deal_size_max = undefined
    this.negotiation_status = []
    this.nature_of_deal = []
    this.investor_id = undefined
    this.investor_country_id = undefined
    this.initiation_year_min = undefined
    this.initiation_year_max = undefined
    this.initiation_year_unknown = true
    this.implementation_status = []
    this.intention_of_investment = []
    this.produce = []
    this.transnational = null
    this.forest_concession = null
    this.carbon_offset_project = null
    this.produce_info_carbon_offsetting = null
    return this
  }

  public isEmpty() {
    // quick fix for now -> todo later: make FilterValues obj not class !!!
    return JSON.stringify(this) === JSON.stringify(new FilterValues().empty())
  }

  public default() {
    // Deal size greater or equal 200ha
    // OR?! { field: "intended_size", operation: "GE", value: "200" },
    // NOTE: this might not work like before because we leave out the "intended_size"
    this.deal_size_min = 200
    // Negotiation Status "Concluded"
    this.negotiation_status = [
      "ORAL_AGREEMENT",
      "CONTRACT_SIGNED",
      "CHANGE_OF_OWNERSHIP",
    ]
    // Exclude Pure Contract Farming
    this.nature_of_deal = [
      "OUTRIGHT_PURCHASE",
      "LEASE",
      "CONCESSION",
      "EXPLOITATION_PERMIT",
    ]
    // Initiation Year unknown or >=2000
    this.initiation_year_min = 2000
    // Exclude: Oil / Gas extraction & Mining
    this.intention_of_investment = [
      // agriculture
      "BIOFUELS",
      "BIOMASS_ENERGY_GENERATION",
      "FODDER",
      "FOOD_CROPS",
      "LIVESTOCK",
      "NON_FOOD_AGRICULTURE",
      "AGRICULTURE_UNSPECIFIED",
      // forest
      "BIOMASS_ENERGY_PRODUCTION",
      "CARBON",
      "FOREST_LOGGING",
      "TIMBER_PLANTATION",
      "FORESTRY_UNSPECIFIED",
      // renewable
      "SOLAR_PARK",
      "WIND_FARM",
      "RENEWABLE_ENERGY",
      // other
      "CONVERSATION",
      "INDUSTRY",
      "LAND_SPECULATION",
      "TOURISM",
      "OTHER",
    ]
    // Transnational True
    this.transnational = true
    // Forest concession False
    this.forest_concession = false
    this.carbon_offset_project = null
    this.produce_info_carbon_offsetting = null
    return this
  }

  public copyNoCountry(other: FilterValues) {
    this.region_id = undefined
    this.country_id = undefined
    this.deal_size_min = other.deal_size_min
    this.deal_size_max = other.deal_size_max
    this.negotiation_status = other.negotiation_status
    this.nature_of_deal = other.nature_of_deal
    this.investor_id = other.investor_id
    this.investor_country_id = other.investor_country_id
    this.initiation_year_min = other.initiation_year_min
    this.initiation_year_max = other.initiation_year_max
    this.initiation_year_unknown = other.initiation_year_unknown
    this.implementation_status = other.implementation_status
    this.intention_of_investment = other.intention_of_investment
    this.produce = other.produce
    this.transnational = other.transnational
    this.forest_concession = other.forest_concession
    return this
  }

  public isDefault() {
    function _equal<T>(a: Array<T>, b: Array<T>) {
      return a.length === b.length && [...a].every(value => b.includes(value))
    }

    return [
      this.deal_size_min === 200,
      !this.deal_size_max,
      _equal(this.negotiation_status, [
        "ORAL_AGREEMENT",
        "CONTRACT_SIGNED",
        "CHANGE_OF_OWNERSHIP",
      ] satisfies NegotiationStatus[]),
      _equal(this.nature_of_deal, [
        "OUTRIGHT_PURCHASE",
        "LEASE",
        "CONCESSION",
        "EXPLOITATION_PERMIT",
      ] satisfies NatureOfDeal[]),
      !this.investor_id,
      !this.investor_country_id,
      this.initiation_year_min === 2000,
      !this.initiation_year_max,
      this.initiation_year_unknown,
      this.implementation_status.length === 0,
      _equal(this.intention_of_investment, [
        // agriculture
        "BIOFUELS",
        "BIOMASS_ENERGY_GENERATION",
        "FODDER",
        "FOOD_CROPS",
        "LIVESTOCK",
        "NON_FOOD_AGRICULTURE",
        "AGRICULTURE_UNSPECIFIED",
        // forest
        "BIOMASS_ENERGY_PRODUCTION",
        "CARBON",
        "FOREST_LOGGING",
        "TIMBER_PLANTATION",
        "FORESTRY_UNSPECIFIED",
        // renewable
        "SOLAR_PARK",
        "WIND_FARM",
        "RENEWABLE_ENERGY",
        // other
        "CONVERSATION",
        "INDUSTRY",
        "LAND_SPECULATION",
        "TOURISM",
        "OTHER",
      ] satisfies IntentionOfInvestment[]),
      !this.produce || this.produce.length === 0,
      this.transnational === true,
      this.forest_concession === false,
      this.carbon_offset_project === null,
      this.produce_info_carbon_offsetting === null,
    ].every(Boolean)
  }
  public toRESTFilterArray() {
    const searchParams = new URLSearchParams()

    if (this.region_id) searchParams.append("region_id", this.region_id.toString())

    if (this.country_id) searchParams.append("country_id", this.country_id.toString())

    if (this.deal_size_min)
      searchParams.append("area_min", this.deal_size_min.toString())

    if (this.deal_size_max)
      searchParams.append("area_max", this.deal_size_max.toString())

    this.negotiation_status.forEach(x =>
      searchParams.append("negotiation_status", x.toString()),
    )
    this.implementation_status.forEach(x =>
      searchParams.append("implementation_status", x.toString()),
    )

    if (this.investor_id)
      searchParams.append("parent_company", this.investor_id.toString())

    if (this.investor_country_id)
      searchParams.append(
        "parent_company_country_id",
        this.investor_country_id.toString(),
      )

    this.nature_of_deal.forEach(x => searchParams.append("nature", x.toString()))

    if (this.initiation_year_min && this.initiation_year_min > 1970)
      searchParams.append("initiation_year_min", this.initiation_year_min.toString())
    if (this.initiation_year_max)
      searchParams.append("initiation_year_max", this.initiation_year_max.toString())
    if (this.initiation_year_min || this.initiation_year_max)
      if (this.initiation_year_unknown) searchParams.append("initiation_year_null", "t")

    this.intention_of_investment.forEach(x =>
      searchParams.append("intention_of_investment", x.toString()),
    )

    if (this.produce && this.produce.length > 0) {
      const crops: string[] = []
      const animals: string[] = []
      const minerals: string[] = []
      for (const prod of this.produce) {
        if (prod.groupId === ProduceGroup.CROPS) crops.push(prod.value)
        else if (prod.groupId === ProduceGroup.ANIMALS) animals.push(prod.value)
        else if (prod.groupId === ProduceGroup.MINERAL_RESOURCES)
          minerals.push(prod.value)
      }
      crops.forEach(c => searchParams.append("crops", c))
      animals.forEach(c => searchParams.append("animals", c))
      minerals.forEach(c => searchParams.append("minerals", c))
    }

    if (this.transnational !== null)
      searchParams.append("transnational", this.transnational.toString())

    if (this.forest_concession !== null)
      searchParams.append("forest_concession", this.forest_concession.toString())

    if (this.carbon_offset_project !== null)
      searchParams.append(
        "carbon_offset_project",
        this.carbon_offset_project.toString(),
      )

    if (this.produce_info_carbon_offsetting !== null)
      searchParams.append(
        "produce_info_carbon_offsetting",
        this.produce_info_carbon_offsetting.toString(),
      )

    return searchParams.toString()
  }
}

export const filters = writable<FilterValues>(new FilterValues().default())
export const publicOnly = writable(true)
export const isDefaultFilter = derived(
  filters,
  $filters => $filters && $filters.isDefault(),
)

export const hydrateAndSubscribeFilterValuesFromLS = () => {
  const filterValuesFromLS = localStorage && localStorage.getItem("filters")
  if (filterValuesFromLS) {
    filters.set(new FilterValues(JSON.parse(filterValuesFromLS)))
  }
  filters.subscribe(
    filterValues =>
      localStorage && localStorage.setItem("filters", JSON.stringify(filterValues)),
  )
}

if (browser) {
  hydrateAndSubscribeFilterValuesFromLS()
}
