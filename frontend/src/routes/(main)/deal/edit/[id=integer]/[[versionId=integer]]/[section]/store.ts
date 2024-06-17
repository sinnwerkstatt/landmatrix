import { writable } from "svelte/store"

import type { DealHull } from "$lib/types/data"

type Mutable<Type> = {
  -readonly [Key in keyof Type]: Mutable<Type[Key]>
}

export type MutableDeal = Mutable<DealHull>
export const mutableDeal = writable<MutableDeal>()
