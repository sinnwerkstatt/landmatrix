import { derived, get, writable } from "svelte/store"

import { browser } from "$app/environment"
import { page } from "$app/stores"

import { allUsers } from "$lib/stores"
import { loading } from "$lib/stores/basics"

import { filters, FilterValues, lastRESTFilterArray } from "./filters"
import { sentenceToArray } from "./helpers"

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

// allUsers derived store with more convenient info
export const users = derived(allUsers, $allUsers => {
  let res = []
  $allUsers.forEach(user => {
    let obj = {
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
// Deals (fetch deals whenever the filters change)
export const deals = writable([])
// export const deals = derived(
//   [filters, lastRESTFilterArray],
//   ([$filters, $lastRESTFilterArray], set) => {
//     const restFilterArray = $filters.toRESTFilterArray()
//     if (browser && restFilterArray != $lastRESTFilterArray) {
//       loading.set(true)
//       fetch(`/api/accountability/deal/?${restFilterArray}`)
//         .then(res => res.json())
//         .then(res => {
//           lastRESTFilterArray.set(restFilterArray)
//           loading.set(false)
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

// =======================================================================================
// Scoring drawer
export const currentDeal = writable<number>()
export const currentVariable = writable<number>()
export const openDrawer = writable<boolean>(false)
