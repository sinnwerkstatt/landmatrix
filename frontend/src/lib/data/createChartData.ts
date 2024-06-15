import type { ChartData } from "chart.js"

import type { AnyKey, BucketMap, SortBy } from "$lib/data/buckets"
import { createEmptyBuckets, sortBuckets } from "$lib/data/buckets"
import type { DealVersion2 } from "$lib/types/data"

export const COLORS = {
  BLACK: "#000000FF",
  BROWN: "#3B2408FF",
  ORANGE: "#FC941FFF",
  ORANGE_LIGHT: "#FC941FB2",
  ORANGE_LIGHTER: "#FC941F66",
  ORANGE_DARK: "#7D4A0FFF",
}

export type DealReducer<TKey extends AnyKey> = (
  acc: BucketMap<TKey>,
  deal: DealVersion2,
) => BucketMap<TKey>

type MapFn<TKey extends AnyKey> =
  | ((key: TKey) => string)
  | ((key: TKey, index: number, array: TKey[]) => string)

export const createChartData =
  <TKey extends AnyKey>(
    dealReducer: DealReducer<TKey>,
    bucketKeys: TKey[],
    labelFn: MapFn<TKey>,
    colorFn: MapFn<TKey>,
  ) =>
  (deals: DealVersion2[], sortBy: SortBy): ChartData<"pie"> => {
    const bucketMap = deals.reduce(dealReducer, createEmptyBuckets(bucketKeys))
    const [keys, buckets] = sortBuckets(sortBy, bucketMap)

    return {
      labels: keys.map(labelFn),
      datasets: [
        {
          data: buckets.map(bucket => bucket[sortBy]),
          backgroundColor: keys.map(colorFn),
        },
      ],
    }
  }
