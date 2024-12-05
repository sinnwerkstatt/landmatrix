import { writable } from "svelte/store"

import type { MutableInvestorHull } from "$lib/types/data"

export const mutableInvestor = writable<MutableInvestorHull>()
