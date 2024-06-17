import { writable } from "svelte/store"

import type { components } from "$lib/openAPI"

type Mutable<Type> = {
  -readonly [Key in keyof Type]: Mutable<Type[Key]>
}

export type MutableInvestor = Mutable<components["schemas"]["Investor"]>
export const mutableInvestor = writable<MutableInvestor>()
