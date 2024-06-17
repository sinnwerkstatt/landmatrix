import { writable } from "svelte/store"

import type { MutableDealHull } from "$lib/types/data"

export const mutableDeal = writable<MutableDealHull>()
