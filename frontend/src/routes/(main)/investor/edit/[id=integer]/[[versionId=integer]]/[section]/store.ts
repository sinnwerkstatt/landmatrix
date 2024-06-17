import { writable } from "svelte/store"

import type { InvestorHull } from "$lib/types/data"

type Mutable<Type> = {
  -readonly [Key in keyof Type]: Mutable<Type[Key]>
}

export type MutableInvestor = Mutable<InvestorHull>
export const mutableInvestor = writable<MutableInvestor>()
