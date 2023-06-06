import * as R from "ramda"

import type { BaseItem } from "$lib/types/deal"

export type Item = BaseItem | Record<string, unknown>

export type Dated<T extends Item> = T & { date: string }
export type IsCurrent<T extends Item> = T & { current: true }

export const isValidDate: (date: string) => boolean = R.pipe(
  R.constructN(1, Date),
  R.invoker(0, "getTime"),
  R.complement(isNaN),
)

export const parseDate: (date: string) => number = R.pipe(
  R.constructN(1, Date),
  R.invoker(0, "getFullYear"),
)

// typeguard 'is' signature not compatible with ramda types -> cast to any
export const isCurrent: <T extends Item>(item: T) => item is IsCurrent<T> = R.propOr(
  false,
  "current",
) as any // eslint-disable-line @typescript-eslint/no-explicit-any

export const isDated: <T extends Item>(item: T) => item is Dated<T> = R.propSatisfies(
  isValidDate,
  "date",
) as any // eslint-disable-line @typescript-eslint/no-explicit-any

export const getFirstByDate = <T extends Item>(items: T[]): Dated<T> | undefined =>
  R.pipe<[T[]], Dated<T>[], Dated<T>[], Dated<T> | undefined>(
    R.filter<T, Dated<T>>(isDated),
    R.sortBy(R.prop("date")),
    R.head,
  )(items)

export const getLastByDate = <T extends Item>(items: T[]): Dated<T> | undefined =>
  R.pipe<[T[]], Dated<T>[], Dated<T>[], Dated<T> | undefined>(
    R.filter<T, Dated<T>>(isDated),
    R.sortBy(R.prop("date")),
    R.last,
  )(items)

export const getCurrent: <T extends Item>(item: T[]) => IsCurrent<T> | undefined =
  R.find(isCurrent)
