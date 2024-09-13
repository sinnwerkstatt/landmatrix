import { get } from "svelte/store"

import { loading } from "$lib/stores/basics"

import { FilterValues, lastRESTFilterArray } from "./filters"
import { deals } from "./stores"

export async function fetchDeals(filters: FilterValues) {
  const restFilterArray = filters.toRESTFilterArray()
  const lastFilterArray = get(lastRESTFilterArray)
  loading.set(true)
  if (restFilterArray != lastFilterArray) {
    try {
      const res = await fetch(`/api/accountability/deal/?${restFilterArray}`)
      const resJSON = await res.json()
      lastRESTFilterArray.set(restFilterArray)
      loading.set(false)
      deals.set(resJSON)
    } catch (error) {
      return error
    }
  }
}
