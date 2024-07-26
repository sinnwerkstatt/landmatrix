import { writable } from "svelte/store"

export class FilterValues {
  region_id?: number[] = []
  country_id?: number[] = []
  area_min?: number
  area_max?: number
  negotiation_status: string[] = []
  nature_of_deal: string[] = []
  investor_id?: number[] = []
  investor_country_id?: number[] = []
  initiation_year_min?: number
  initiation_year_max?: number
  initiation_year_unknown = true
  implementation_status: string[] = []
  intention_of_investment: string[] = []
  intention_of_investment_unknown: boolean = false
  crops?: string[] = []
  animals?: string[] = []
  minerals?: string[] = []
  transnational: boolean | null = null
  forest_concession: boolean | null = null

  public empty() {
    this.region_id = []
    this.country_id = []
    this.area_min = undefined
    this.area_max = undefined
    this.negotiation_status = []
    this.nature_of_deal = []
    this.investor_id = []
    this.investor_country_id = []
    this.initiation_year_min = undefined
    this.initiation_year_max = undefined
    this.initiation_year_unknown = true
    this.implementation_status = []
    this.intention_of_investment = []
    this.intention_of_investment_unknown = false
    this.crops = []
    this.animals = []
    this.minerals = []
    this.transnational = null
    this.forest_concession = null
    return this
  }

  public default() {
    this.area_min = 200
    this.negotiation_status = [
      "ORAL_AGREEMENT",
      "CONTRACT_SIGNED",
      "CHANGE_OF_OWNERSHIP",
    ]
    this.nature_of_deal = [
      "OUTRIGHT_PURCHASE",
      "LEASE",
      "CONCESSION",
      "EXPLOITATION_PERMIT",
    ]
    this.initiation_year_min = 2000
    this.intention_of_investment = [
      "BIOFUELS",
      "BIOMASS_ENERGY_GENERATION",
      "FODDER",
      "FOOD_CROPS",
      "LIVESTOCK",
      "NON_FOOD_AGRICULTURE",
      "AGRICULTURE_UNSPECIFIED",
      "BIOMASS_ENERGY_PRODUCTION",
      "CARBON",
      "FOREST_LOGGING",
      "TIMBER_PLANTATION",
      "FORESTRY_UNSPECIFIED",
      "SOLAR_PARK",
      "WIND_FARM",
      "RENEWABLE_ENERGY",
      "CONVERSATION",
      "INDUSTRY",
      "LAND_SPECULATION",
      "TOURISM",
      "OTHER",
    ]
    this.transnational = true
    this.forest_concession = false
    return this
  }

  public toRESTFilterArray() {
    const searchParams = new URLSearchParams()

    this.country_id?.forEach(e => searchParams.append("country_id", e.toString()))

    return searchParams.toString()
  }
}

export const filters = writable<FilterValues>(new FilterValues())
export const lastRESTFilterArray = writable<string | null>(null)
