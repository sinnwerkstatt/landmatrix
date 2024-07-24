import { derived, writable } from "svelte/store"

import { browser } from "$app/environment"

import { loading } from "$lib/stores/basics"

import { filters, lastRESTFilterArray } from "./filters"

// Navigation status
export const openedFilterBar = writable(false)

// Deals navigation history (remember the last opened project and deal for faster navigation between tabs and sessions)
const currentDealsHistory = browser
  ? window.localStorage.getItem("currentDealHistory") ?? "/accountability/deals/0/"
  : "/accountability/deals/0/"

export const dealsHistory = writable<string>(currentDealsHistory)

dealsHistory.subscribe(value => {
  if (browser) {
    window.localStorage.setItem("currentDealHistory", value)
  }
})

// =======================================================================================
// Deals (fetch deals whenever the filters change)
export const deals = derived(
  [filters, lastRESTFilterArray],
  ([$filters, $lastRESTFilterArray], set) => {
    const restFilterArray = $filters.toRESTFilterArray()
    if (restFilterArray != $lastRESTFilterArray) {
      loading.set(true)
      fetch(`/api/accountability/deal/?${restFilterArray}`)
        .then(res => res.json())
        .then(res => {
          lastRESTFilterArray.set(restFilterArray)
          loading.set(false)
          set(res)
        })
    }
  },
  [],
)

// =======================================================================================
// Documentation bookmark
export const documentationBookmark = writable(undefined)

// =======================================================================================
// Table selection from Deals/Scoring
export const tableSelection = writable({})

// =======================================================================================
// Scoring drawer
export const currentDeal = writable<number>()
export const currentVariable = writable<number>()
export const openDrawer = writable<boolean>(false)
