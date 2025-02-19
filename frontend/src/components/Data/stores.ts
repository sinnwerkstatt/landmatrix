import { writable, type Writable } from "svelte/store"

import type { Model, MutableDealHull, MutableInvestorHull } from "$lib/types/data"

export const showFilterBar = writable(true)
export const showContextBar = writable(true)

const mutableObjects = {
  deal: writable<MutableDealHull>(),
  investor: writable<MutableInvestorHull>(),
} satisfies { [key in Model]: Writable<object> }

export const getMutableObject: <T extends Model>(
  model: T,
) => (typeof mutableObjects)[T] = model => mutableObjects[model]

// type StoreValueType<T> = T extends Writable<infer U> ? U : never;
