import { createBucketMap, createBucketMapReducer, sortBuckets } from "$lib/data/buckets"

describe("buckets", () => {
  test("createBuckets", () => {
    type Key = "a" | "b"
    const keys: Key[] = ["a", "b", "a"]

    const bucketMap = createBucketMap(keys)

    expect(bucketMap).toEqual({
      a: { size: 0, count: 0 },
      b: { size: 0, count: 0 },
    })
  })

  test("createBucketMapReducer", () => {
    type Key = "a" | "b"
    const keys: Key[] = ["a", "b", "a"]

    const bucketMapReducer = createBucketMapReducer<Key>(2)
    const bucketMap = keys.reduce(bucketMapReducer, {
      a: { size: 0, count: 0 },
      b: { size: 0, count: 0 },
    })

    expect(bucketMap).toEqual({
      a: { size: 4, count: 2 },
      b: { size: 2, count: 1 },
    })
  })

  test("sortBuckets", () => {
    const bucketMap = {
      a: { size: 5, count: 1 },
      b: { size: 10, count: 3 },
      c: { size: 1, count: 2 },
    }

    const [keysBySize, bucketsBySize] = sortBuckets("size", bucketMap)

    expect(keysBySize).toEqual(["b", "a", "c"])
    expect(bucketsBySize).toEqual([
      { size: 10, count: 3 },
      { size: 5, count: 1 },
      { size: 1, count: 2 },
    ])

    const [keysByCount, bucketsByCount] = sortBuckets("count", bucketMap)

    expect(keysByCount).toEqual(["b", "c", "a"])
    expect(bucketsByCount).toEqual([
      { size: 10, count: 3 },
      { size: 1, count: 2 },
      { size: 5, count: 1 },
    ])
  })
})
