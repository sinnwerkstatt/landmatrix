import { writable } from "svelte/store"

import type { DealHull } from "$lib/types/newtypes"

export const mutableDeal = writable<DealHull>()
