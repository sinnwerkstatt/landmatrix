import * as R from "ramda"

import { IoIGroup, IoI } from "$lib/types/deal"
import type { Bucket, SortBy, BucketMap } from "$lib/data/buckets"
import {
  flat_intention_of_investment_map,
  intention_of_investment_group_choices,
} from "$lib/choices"
import { sumBuckets } from "$lib/data/buckets"

const toggleSortBy = (sortBy: SortBy): SortBy => (sortBy === "count" ? "size" : "count")

export const IOI_GROUP_COLORS: {
  [key in IoIGroup]: string
} = {
  [IoIGroup.FORESTRY]: "#179961",
  [IoIGroup.AGRICULTURE]: "#00bfff",
  [IoIGroup.OTHER]: "#ff7c63",
}
export type GroupedBuckets = { [key in IoIGroup]: BucketMap<IoI> }
export type GroupedEntries = [IoIGroup, [IoI, Bucket][]][]
export const getSortedEntries = (
  sortBy: SortBy,
  grouped: GroupedBuckets,
): GroupedEntries =>
  Object.entries<BucketMap>(grouped)
    // .sort(
    //   (entry1, entry2) =>
    //     sumBuckets(entry2[1])[sortBy] - sumBuckets(entry1[1])[sortBy],
    // )
    .map(([key, value]) => [
      key,
      Object.entries(value).sort(
        (entry1, entry2) => entry2[1][sortBy] - entry1[1][sortBy],
      ),
    ]) as GroupedEntries

export interface Item<Key extends string = string> {
  key: Key
  value: number
  label: string
}
import { get } from "svelte/store"
import type { Readable } from "svelte/store"
export const createData = (
  _: Readable<any>,
  sortBy: SortBy,
): ((entries: GroupedEntries) => Item<IoI>[]) =>
  R.pipe(
    R.map(R.nth(1)),
    R.unnest,
    R.map<[IoI, Bucket], Item<IoI>>(
      ([key, bucket]) =>
        ({
          key,
          value: bucket[sortBy],
          label: get(_)(flat_intention_of_investment_map[key]),
        } as Item<IoI>),
    ),
    normalize,
  )

export const createGroupData = (_, sortBy: SortBy) =>
  R.pipe(
    R.map(([key, value]) => {
      return {
        key,
        value: R.pipe(R.map(R.nth(1)), sumBuckets, R.prop(sortBy))(value),
        label: get(_)(intention_of_investment_group_choices[key]),
      } as Item<IoIGroup>
    }),
    normalize,
  )

const normalize = (items: Item[]) => {
  const total = R.pipe<[Item[]], number[], number>(R.map(R.prop("value")), R.sum)(items)
  return items.map(item => ({
    ...item,
    value: item["value"] / total,
  }))
}

export const createBackgroundColors: (entries: GroupedEntries) => string[] = R.pipe(
  R.map(([key, value]) => {
    const color = IOI_GROUP_COLORS[key]
    const count = Object.values(value).length
    return R.range(0, count).map(
      i => color + (((count - i) / (count + 1)) * 100).toFixed(0),
    )
  }),
  R.unnest,
)
