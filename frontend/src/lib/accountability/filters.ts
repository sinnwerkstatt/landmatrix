import { writable } from "svelte/store"

export class FilterValues {
  region_id?: number[] = []
  country_id?: number[] = []
  deal_size_min?: number
  deal_size_max?: number
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
  produce?: string[] = []
  transnational: boolean | null = null
  forest_concession: boolean | null = null

  public toRESTFilterArray() {
    const searchParams = new URLSearchParams()

    this.country_id?.forEach(e => searchParams.append("country_id", e.toString()))

    return searchParams.toString()
  }
}

export const filters = writable<FilterValues>(new FilterValues())
export const lastRESTFilterArray = writable<string | null>(null)
