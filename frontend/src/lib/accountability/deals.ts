import { get, writable } from "svelte/store"

import { FilterValues, lastRESTFilterArray } from "./filters"
import { deals } from "./stores"

export const loadingDeals = writable(false)

export async function fetchDeals(filters: FilterValues) {
  const restFilterArray = filters.toRESTFilterArray()
  const lastFilterArray = get(lastRESTFilterArray)
  loadingDeals.set(true)
  if (restFilterArray != lastFilterArray) {
    try {
      const res = await fetch(`/api/accountability/deal/?${restFilterArray}`)
      const resJSON = await res.json()
      lastRESTFilterArray.set(restFilterArray)
      loadingDeals.set(false)
      deals.set(resJSON)
    } catch (error) {
      loadingDeals.set(false)
      return error
    }
  }
}

export async function fetchDealDetail(id: number) {
  try {
    const res = await fetch(`/api/deals/${id}/`)
    const resJSON = await res.json()
    return resJSON
  } catch (error) {
    return error
  }
}
