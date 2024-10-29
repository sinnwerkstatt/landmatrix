import { derived, get, writable } from "svelte/store"

import { browser } from "$app/environment"
import { page } from "$app/stores"

import { allUsers } from "$lib/stores"

// import { filters, FilterValues, lastRESTFilterArray } from "./filters"
import { sentenceToArray } from "./helpers"

// Navigation status
export const openedFilterBar = writable(true)

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

// allUsers derived store with more convenient info + filter only editor and above
export const users = derived(allUsers, $allUsers => {
  const res = []
  $allUsers.forEach(user => {
    if (user.role >= 2) {
      const obj = {
        id: user.id,
        name: user.full_name ? user.full_name : user.username,
      }

      // Initials from usernames
      const names = sentenceToArray(obj.name)
      if (names?.length == 1) {
        obj.initials = obj.name.substring(0, 2).toUpperCase()
      } else if (names?.length > 1) {
        const first = names?.at(0).substring(0, 1).toUpperCase()
        const last = names
          ?.at(names.length - 1)
          .substring(0, 1)
          .toUpperCase()
        obj.initials = first + last
      }

      res.push(obj)
    }
  })
  return res
})

export const me = derived(
  users,
  ($users, set) => {
    const pageData = get(page)
    const userData: { id: number; name: string; intials: string }[] = $users
    set(userData.filter(u => u.id == pageData.data.user.id)[0])
  },
  {},
)

// =======================================================================================
// Deals
export const deals = writable([])
export const loadingDeals = writable(false)

// Store that fetches deals when the filters change but value is stores in deals store (above) or it's not locally editable
// export const dealsStore = derived(
//   [filters, lastRESTFilterArray],
//   ([$filters, $lastRESTFilterArray], set) => {
//     const restFilterArray = $filters.toRESTFilterArray()
//     if (browser && restFilterArray != $lastRESTFilterArray) {
//       loadingDeals.set(true)
//       fetch(`/api/accountability/deal/?${restFilterArray}`)
//         .then(res => res.json())
//         .then(res => {
//           lastRESTFilterArray.set(restFilterArray)
//           loadingDeals.set(false)
//           deals.set(res)
//           set(res)
//         })
//     }
//   },
//   [],
// )

// =======================================================================================
// Documentation bookmark
export const documentationBookmark = writable(undefined)

// =======================================================================================
// Table selection from Deals/Scoring
export const tableSelection = writable({})
export const tableSelectionChecked = derived(tableSelection, $tableSelection => {
  const checked = []
  Object.keys($tableSelection).forEach(d => {
    Object.keys($tableSelection[d].variables).forEach(v => {
      if ($tableSelection[d].variables[v]) checked.push({ deal: d, variable: v })
    })
  })
  return checked
})

// =======================================================================================
// Scoring drawer
export const currentDeal = writable<number>()
export const currentVariable = writable<number>()
export const openDrawer = writable<boolean>(false)
