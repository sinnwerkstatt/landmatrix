import { derived, writable } from "svelte/store"

import { browser } from "$app/environment"

import {
  ImplementationStatus,
  IntentionOfInvestment,
  NatureOfDeal,
  NegotiationStatus,
  ProduceGroup,
} from "$lib/types/deal"

import type { GQLFilter } from "./types/filters"
import type { Investor } from "./types/investor"

export interface Produce {
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
  investor?: Investor
  investor_country_id?: number
  initiation_year_min?: number
  initiation_year_max?: number
  initiation_year_unknown = true
  implementation_status: ImplementationStatus[] = []
  intention_of_investment: IntentionOfInvestment[] = []
  produce?: Produce[] = []
  transnational: boolean | null = null
  forest_concession: boolean | null = null

  constructor(data: Partial<FilterValues> = {}) {
    Object.assign(this, data)
  }

  public empty() {
    this.deal_size_min = undefined
    this.deal_size_max = undefined
    this.negotiation_status = []
    this.nature_of_deal = []
    this.investor = undefined
    this.investor_country_id = undefined
    this.initiation_year_min = undefined
    this.initiation_year_max = undefined
    this.initiation_year_unknown = true
    this.implementation_status = []
    this.intention_of_investment = []
    this.produce = []
    this.transnational = null
    this.forest_concession = null
    return this
  }

  public default() {
    // Deal size greater or equal 200ha
    // OR?! { field: "intended_size", operation: "GE", value: "200" },
    // NOTE: this might not work like before because we leave out the "intended_size"
    this.deal_size_min = 200
    // Negotiation Status "Concluded"
    this.negotiation_status = [
      NegotiationStatus.ORAL_AGREEMENT,
      NegotiationStatus.CONTRACT_SIGNED,
      NegotiationStatus.CHANGE_OF_OWNERSHIP,
    ]
    // Exclude Pure Contract Farming
    this.nature_of_deal = [
      NatureOfDeal.OUTRIGHT_PURCHASE,
      NatureOfDeal.LEASE,
      NatureOfDeal.CONCESSION,
      NatureOfDeal.EXPLOITATION_PERMIT,
    ]
    // Initiation Year unknown or >=2000
    this.initiation_year_min = 2000
    // Exclude: Oil / Gas extraction & Mining
    this.intention_of_investment = [
      // agriculture
      IntentionOfInvestment.BIOFUELS,
      IntentionOfInvestment.BIOMASS_ENERGY_GENERATION,
      IntentionOfInvestment.FODDER,
      IntentionOfInvestment.FOOD_CROPS,
      IntentionOfInvestment.LIVESTOCK,
      IntentionOfInvestment.NON_FOOD_AGRICULTURE,
      IntentionOfInvestment.AGRICULTURE_UNSPECIFIED,
      // forest
      IntentionOfInvestment.BIOMASS_ENERGY_PRODUCTION,
      IntentionOfInvestment.CARBON,
      IntentionOfInvestment.FOREST_LOGGING,
      IntentionOfInvestment.TIMBER_PLANTATION,
      IntentionOfInvestment.FORESTRY_UNSPECIFIED,
      // renewable
      IntentionOfInvestment.SOLAR_PARK,
      IntentionOfInvestment.WIND_FARM,
      IntentionOfInvestment.RENEWABLE_ENERGY,
      // other
      IntentionOfInvestment.CONVERSATION,
      IntentionOfInvestment.INDUSTRY,
      IntentionOfInvestment.LAND_SPECULATION,
      IntentionOfInvestment.TOURISM,
      IntentionOfInvestment.OTHER,
    ]
    // Transnational True
    this.transnational = true
    // Forest concession False
    this.forest_concession = false
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
        NegotiationStatus.ORAL_AGREEMENT,
        NegotiationStatus.CONTRACT_SIGNED,
        NegotiationStatus.CHANGE_OF_OWNERSHIP,
      ]),
      _equal(this.nature_of_deal, [
        NatureOfDeal.OUTRIGHT_PURCHASE,
        NatureOfDeal.LEASE,
        NatureOfDeal.CONCESSION,
        NatureOfDeal.EXPLOITATION_PERMIT,
      ]),
      !this.investor,
      !this.investor_country_id,
      this.initiation_year_min === 2000,
      !this.initiation_year_max,
      this.initiation_year_unknown,
      this.implementation_status.length === 0,
      _equal(this.intention_of_investment, [
        IntentionOfInvestment.BIOFUELS,
        IntentionOfInvestment.BIOMASS_ENERGY_GENERATION,
        IntentionOfInvestment.FOOD_CROPS,
        IntentionOfInvestment.FODDER,
        IntentionOfInvestment.LIVESTOCK,
        IntentionOfInvestment.NON_FOOD_AGRICULTURE,
        IntentionOfInvestment.AGRICULTURE_UNSPECIFIED,
        IntentionOfInvestment.TIMBER_PLANTATION,
        IntentionOfInvestment.FOREST_LOGGING,
        IntentionOfInvestment.CARBON,
        IntentionOfInvestment.FORESTRY_UNSPECIFIED,
        IntentionOfInvestment.TOURISM,
        IntentionOfInvestment.INDUSTRY,
        IntentionOfInvestment.CONVERSATION,
        IntentionOfInvestment.LAND_SPECULATION,
        IntentionOfInvestment.RENEWABLE_ENERGY,
        IntentionOfInvestment.OTHER,
      ]),
      !this.produce || this.produce.length === 0,
      this.transnational === true,
      this.forest_concession === false,
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

    if (this.investor)
      searchParams.append("parent_company", this.investor.id.toString())

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
        if (prod.groupID === ProduceGroup.CROPS) crops.push(prod.value)
        else if (prod.groupID === ProduceGroup.ANIMALS) animals.push(prod.value)
        else if (prod.groupID === ProduceGroup.MINERAL_RESOURCES)
          minerals.push(prod.value)
      }
      crops.forEach(c => searchParams.append("crops", c))
      animals.forEach(c => searchParams.append("animals", c))
      minerals.forEach(c => searchParams.append("minerals", c))
    }

    if (this.transnational !== null)
      searchParams.append("trans", this.transnational.toString())

    if (this.forest_concession !== null)
      searchParams.append("for_con", this.forest_concession.toString())

    return searchParams.toString()
  }

  public toGQLFilterArray(): GQLFilter[] {
    const filterArray: GQLFilter[] = []

    if (this.region_id)
      filterArray.push({ field: "country.region_id", value: this.region_id })

    if (this.country_id)
      filterArray.push({ field: "country_id", value: this.country_id })

    if (this.deal_size_min)
      filterArray.push({
        field: "deal_size",
        operation: "GE",
        value: this.deal_size_min,
      })

    if (this.deal_size_max)
      filterArray.push({
        field: "deal_size",
        operation: "LE",
        value: this.deal_size_max,
      })

    if (this.negotiation_status.length > 0)
      filterArray.push({
        field: "current_negotiation_status",
        operation: "IN",
        value: this.negotiation_status,
      })

    if (this.implementation_status.length > 0)
      filterArray.push({
        field: "current_implementation_status",
        operation: "IN",
        value: this.implementation_status,
        allow_null: this.implementation_status.includes(
          "UNKNOWN" as ImplementationStatus,
        ),
      })

    if (this.investor)
      filterArray.push({ field: "parent_companies", value: this.investor.id })

    if (this.investor_country_id)
      filterArray.push({
        field: "parent_companies.country_id",
        value: this.investor_country_id,
      })

    if (this.nature_of_deal.length > 0) {
      const allValues = Object.values(NatureOfDeal)
      const diffValues = allValues.filter(x => !this.nature_of_deal.includes(x))

      if (diffValues.length > 0)
        filterArray.push({
          field: "nature_of_deal",
          operation: "CONTAINED_BY",
          value: diffValues,
          exclusion: true,
        })
    }

    if (this.initiation_year_min && this.initiation_year_min > 1970)
      filterArray.push({
        field: "initiation_year",
        operation: "GE",
        value: this.initiation_year_min,
        allow_null: this.initiation_year_unknown,
      })

    if (this.initiation_year_max)
      filterArray.push({
        field: "initiation_year",
        operation: "LE",
        value: this.initiation_year_max,
        allow_null: this.initiation_year_unknown,
      })

    if (this.intention_of_investment.length > 0) {
      filterArray.push({
        field: "current_intention_of_investment",
        operation: "OVERLAP",
        value: this.intention_of_investment,
        allow_null: this.intention_of_investment.includes(
          "UNKNOWN" as IntentionOfInvestment,
        ),
      })
    }

    if (this.produce && this.produce.length > 0) {
      const crops = []
      const animals = []
      const minerals = []
      for (const prod of this.produce) {
        if (prod.groupId === ProduceGroup.CROPS) crops.push(prod.value)
        else if (prod.groupId === ProduceGroup.ANIMALS) animals.push(prod.value)
        else if (prod.groupId === ProduceGroup.MINERAL_RESOURCES)
          minerals.push(prod.value)
      }
      if (crops.length > 0) {
        filterArray.push({
          field: "current_crops",
          operation: "CONTAINS",
          value: crops,
        })
      }
      if (animals.length > 0) {
        filterArray.push({
          field: "current_animals",
          operation: "CONTAINS",
          value: animals,
        })
      }
      if (minerals.length > 0) {
        filterArray.push({
          field: "current_mineral_resources",
          operation: "CONTAINS",
          value: minerals,
        })
      }
    }

    if (this.transnational !== null)
      filterArray.push({ field: "transnational", value: this.transnational })

    if (this.forest_concession !== null)
      filterArray.push({ field: "forest_concession", value: this.forest_concession })

    return filterArray
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
