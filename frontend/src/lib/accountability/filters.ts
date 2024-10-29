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
  initiation_year_unknown: boolean = true
  implementation_status: string[] = []
  intention_of_investment: string[] = []
  intention_of_investment_unknown: boolean = false
  crops?: string[] = []
  animals?: string[] = []
  minerals?: string[] = []
  transnational: boolean | null = null
  forest_concession: boolean | null = null

  constructor(data: Partial<FilterValues> = {}) {
    const clean = {}
    Object.keys(data).forEach(key => {
      if (data[key] !== undefined) clean[key] = data[key]
    })
    Object.assign(this, clean)
  }

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

    this.region_id?.forEach(e => searchParams.append("region_id", e.toString()))
    this.country_id?.forEach(e => searchParams.append("country_id", e.toString()))

    if (this.area_min) searchParams.append("area_min", this.area_min.toString())
    if (this.area_max) searchParams.append("area_max", this.area_max.toString())

    this.negotiation_status?.forEach(e =>
      searchParams.append("negotiation_status", e.toString()),
    )

    this.nature_of_deal?.forEach(e =>
      searchParams.append("nature_of_deal", e.toString()),
    )

    this.investor_id?.forEach(e => searchParams.append("investor_id", e.toString()))
    this.investor_country_id?.forEach(e =>
      searchParams.append("investor_country_id", e.toString()),
    )

    if (this.initiation_year_min)
      searchParams.append("initiation_year_min", this.initiation_year_min.toString())
    if (this.initiation_year_max)
      searchParams.append("initiation_year_max", this.initiation_year_max.toString())

    if (this.initiation_year_unknown === false) {
      searchParams.append("initiation_year_unknown", "false")
    } else if (this.initiation_year_unknown) {
      searchParams.append("initation_year_unknown", "true")
    }

    this.implementation_status?.forEach(e =>
      searchParams.append("implementation_status", e.toString()),
    )

    this.intention_of_investment?.forEach(e =>
      searchParams.append("intention_of_investment", e.toString()),
    )

    if (this.intention_of_investment_unknown)
      searchParams.append("intention_of_investment", "UNKNOWN")

    this.crops?.forEach(e => searchParams.append("crops", e.toString()))
    this.animals?.forEach(e => searchParams.append("animals", e.toString()))
    this.minerals?.forEach(e => searchParams.append("minerals", e.toString()))

    if (this.transnational !== null)
      searchParams.append("transnational", this.transnational.toString())

    if (this.forest_concession !== null)
      searchParams.append("forest_concession", this.forest_concession.toString())

    return searchParams.toString()
  }
}

export const filters = writable<FilterValues>(new FilterValues())
export const lastRESTFilterArray = writable<string | null>(null)
