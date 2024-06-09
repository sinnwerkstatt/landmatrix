import { writable } from "svelte/store"

import type { components } from "$lib/openAPI"

type Mutable<Type> = {
  -readonly [Key in keyof Type]: Mutable<Type[Key]>
}

export type MutableDeal = Mutable<components["schemas"]["Deal"]>
export const mutableDeal = writable<MutableDeal>()
