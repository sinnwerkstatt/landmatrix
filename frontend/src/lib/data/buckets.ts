export interface Bucket {
  count: number
  size: number
}
export type SortBy = keyof Bucket

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type AnyKey = keyof any

export type BucketMap<TKey extends AnyKey = AnyKey> = { [key in TKey]: Bucket }

export const bucketKeys = <T extends AnyKey>(buckets: BucketMap<T>): T[] =>
  Object.keys(buckets) as T[]

export const bucketValues = <T extends AnyKey>(buckets: BucketMap<T>): Bucket[] =>
  Object.values(buckets)

export const bucketEntries = <T extends AnyKey>(buckets: BucketMap<T>): [T, Bucket][] =>
  Object.entries(buckets) as [T, Bucket][]

export const createEmptyBuckets = <TKey extends AnyKey>(
  keys: TKey[],
): BucketMap<TKey> =>
  keys.reduce(
    (bucketMap, key) => ({
      ...bucketMap,
      [key]: {
        count: 0,
        size: 0,
      },
    }),
    {} as BucketMap<TKey>,
  )

export const createBucketMapReducer =
  <TKey extends AnyKey>(size = 0, count = 1) =>
  (bucketMap: Partial<BucketMap<TKey>> = {}, key: TKey): BucketMap<TKey> => ({
    ...bucketMap,
    [key]: {
      count: (bucketMap[key]?.count || 0) + count,
      size: (bucketMap[key]?.size || 0) + size,
    },
  })

export const sortBuckets = <TKey extends AnyKey>(
  sortBy: SortBy,
  bucketMap: BucketMap<TKey>,
): [TKey[], Bucket[]] => {
  const sorted = bucketEntries(bucketMap).sort(
    (entry1, entry2) => entry2[1][sortBy] - entry1[1][sortBy],
  )
  return [sorted.map(entry => entry[0]), sorted.map(entry => entry[1])]
}

export const sumBuckets = <TKey extends AnyKey>(buckets: BucketMap<TKey>): Bucket =>
  bucketValues(buckets).reduce(
    (sums: Bucket, bucket: Bucket) => ({
      count: sums.count + bucket.count,
      size: sums.size + bucket.size,
    }),
    { count: 0, size: 0 },
  )
