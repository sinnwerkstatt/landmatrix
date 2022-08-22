export interface Bucket {
  count: number;
  size: number;
}
export type SortBy = keyof Bucket;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type AnyKey = keyof any;

export type BucketMap<TKey extends AnyKey = AnyKey> = Partial<Record<TKey, Bucket>>;

export const createBucketMap = <TKey extends AnyKey>(keys: TKey[]): BucketMap<TKey> =>
  keys.reduce(
    (bucketMap, key) => ({
      ...bucketMap,
      [key]: {
        count: 0,
        size: 0,
      },
    }),
    {} as BucketMap<TKey>
  );

export const createBucketMapReducer =
  <TKey extends AnyKey>(size = 0) =>
  (bucketMap: BucketMap<TKey> = {}, key: TKey): BucketMap<TKey> => ({
    ...bucketMap,
    [key]: {
      count: (bucketMap[key]?.count || 0) + 1,
      size: (bucketMap[key]?.size || 0) + size,
    },
  });

export const sortBuckets = <TKey extends AnyKey>(
  sortBy: SortBy,
  bucketMap: BucketMap<TKey>
): [TKey[], Bucket[]] => {
  const entries = Object.entries(bucketMap) as [TKey, Bucket][];
  const sorted = entries.sort(
    (entry1, entry2) => entry2[1][sortBy] - entry1[1][sortBy]
  );
  return [sorted.map((entry) => entry[0]), sorted.map((entry) => entry[1])];
};
