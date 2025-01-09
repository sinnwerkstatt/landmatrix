import { writable } from "svelte/store"

import type { MutableDealHull, MutableInvestorHull } from "$lib/types/data"

export const showFilterBar = writable(true)
export const showContextBar = writable(true)

export const mutableDeal = writable<MutableDealHull>()
export const mutableInvestor = writable<MutableInvestorHull>()
