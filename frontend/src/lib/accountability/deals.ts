import { get, writable } from "svelte/store"

import { browser } from "$app/environment"

import { FilterValues, lastRESTFilterArray } from "./filters"
import { deals, loadingDeals } from "./stores"

export const queryID = writable(0)

export async function fetchDeals(filters: FilterValues) {
  const restFilterArray = filters.toRESTFilterArray()
  const lastFilterArray = get(lastRESTFilterArray)
  loadingDeals.set(true)

  queryID.set(get(queryID) + 1)
  const currentQueryID = get(queryID)

  if (browser && restFilterArray != lastFilterArray) {
    try {
      const res = await fetch(`/api/accountability/deal/?${restFilterArray}`)
      const resJSON = await res.json()
      lastRESTFilterArray.set(restFilterArray)
      if (get(queryID) == currentQueryID) deals.set(resJSON)
    } catch (error) {
      return error
    }
  }

  loadingDeals.set(false)
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
