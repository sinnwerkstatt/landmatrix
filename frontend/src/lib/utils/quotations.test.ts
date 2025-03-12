import { describe, expect, test } from "vitest"

import {
  cleanEmptyBranches,
  getQuotations,
  removeAndCleanQuotations,
  removeQuotations,
  setAndCleanQuotations,
  setQuotations,
  type Quotations,
} from "./quotations"

describe("Quotations Utility Functions", () => {
  const sampleQuotations: Quotations<{ nid: string; other?: number }> = {
    a: {
      b: {
        c1: [{ nid: "1" }, { nid: "2", other: 200 }],
        2: [{ nid: "1", other: -20 }],
        c3: { nested: [{ nid: "3" }] },
      },
    },
  }

  describe("getQuotations", () => {
    test("retrieves an array at the given path", () => {
      expect(getQuotations(sampleQuotations, ["a", "b", "c1"])).toEqual([
        { nid: "1" },
        { nid: "2", other: 200 },
      ])
    })

    test("retrieves a nested object at the given path", () => {
      expect(getQuotations(sampleQuotations, ["a", "b", "c3"])).toEqual({
        nested: [{ nid: "3" }],
      })
    })

    test("returns an empty array for a non-existent path", () => {
      expect(getQuotations(sampleQuotations, ["x", "y", "z"])).toEqual([])
    })

    test("returns the full structure when path is empty", () => {
      expect(getQuotations(sampleQuotations, [])).toEqual(sampleQuotations)
    })

    test("handles incorrect types without throwing", () => {
      expect(getQuotations(sampleQuotations, ["a", "b", "c1", "c3"])).toEqual([])
    })
  })

  describe("setQuotations", () => {
    test("sets a new quotation list at a path", () => {
      expect(
        setQuotations(sampleQuotations, ["a", "b", "c1"], [{ nid: "99" }]),
      ).toEqual({
        a: {
          b: {
            c1: [{ nid: "99" }],
            2: [{ nid: "1", other: -20 }],
            c3: { nested: [{ nid: "3" }] },
          },
        },
      })
    })

    test("sets an entire quotations subtree", () => {
      expect(
        setQuotations(sampleQuotations, ["x"], { y: { z: [{ nid: "3" }] } }),
      ).toEqual({
        ...sampleQuotations,
        x: { y: { z: [{ nid: "3" }] } },
      })
    })

    test("preserves other paths when modifying a nested path", () => {
      expect(
        setQuotations(sampleQuotations, ["a", "b", "c3"], [{ nid: "99" }]),
      ).toEqual({
        a: {
          b: {
            c1: [{ nid: "1" }, { nid: "2", other: 200 }],
            2: [{ nid: "1", other: -20 }],
            c3: [{ nid: "99" }],
          },
        },
      })
    })

    test("overwrites an existing array with a new object", () => {
      expect(
        setQuotations(sampleQuotations, ["a", "b", "c1"], { nested: [{ nid: "4" }] }),
      ).toEqual({
        a: {
          b: {
            c1: { nested: [{ nid: "4" }] },
            2: [{ nid: "1", other: -20 }],
            c3: { nested: [{ nid: "3" }] },
          },
        },
      })
    })
  })

  describe("removeQuotations", () => {
    test("removes all items with the specified nid", () => {
      expect(removeQuotations(sampleQuotations, "1")).toEqual({
        a: {
          b: {
            c1: [{ nid: "2", other: 200 }],
            2: [],
            c3: { nested: [{ nid: "3" }] },
          },
        },
      })
    })

    test("does nothing if the nid does not exist", () => {
      expect(removeQuotations(sampleQuotations, "999")).toEqual(sampleQuotations)
    })
  })

  describe("cleanEmptyBranches", () => {
    test("removes empty arrays", () => {
      const input = { a: { b: { c1: [] } } }
      expect(cleanEmptyBranches(input)).toEqual({})
    })

    test("removes empty objects recursively", () => {
      const input = { a: { b: { c1: [], 2: {} } } }
      expect(cleanEmptyBranches(input)).toEqual({})
    })

    test("preserves valid nodes", () => {
      expect(cleanEmptyBranches(sampleQuotations)).toEqual(sampleQuotations)
    })
  })

  describe("setAndCleanQuotations", () => {
    test("sets a value and removes empty branches when necessary", () => {
      expect(setAndCleanQuotations(sampleQuotations, ["a", "b", "c1"], [])).toEqual({
        a: {
          b: {
            2: [{ nid: "1", other: -20 }],
            c3: { nested: [{ nid: "3" }] },
          },
        },
      })
    })

    test("sets an object and keeps the structure valid", () => {
      expect(
        setAndCleanQuotations(sampleQuotations, ["x"], { y: { z: [{ nid: "3" }] } }),
      ).toEqual({
        ...sampleQuotations,
        x: { y: { z: [{ nid: "3" }] } },
      })
    })
  })

  describe("removeAndCleanQuotations", () => {
    test("removes a nid and cleans up empty structures", () => {
      expect(removeAndCleanQuotations(sampleQuotations, "3")).toEqual({
        a: {
          b: {
            c1: [{ nid: "1" }, { nid: "2", other: 200 }],
            2: [{ nid: "1", other: -20 }],
          },
        },
      })
    })

    test("removes all instances and results in an empty object", () => {
      const input = { a: { b: { c1: [{ nid: "3" }] } } }
      expect(removeAndCleanQuotations(input, "3")).toEqual({})
    })
  })
})
