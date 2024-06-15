import {
  createBuckets,
  createConcludedDealsOverTimeReducer,
  createYearSizeMap,
} from "$lib/data/charts/concludedDealsOverTime"
import type { ContractSizeItem } from "$lib/data/dealUtils"
import type { DealVersion2 } from "$lib/types/data"

describe("Cumulative number of deals", () => {
  test("a.1) Date is given on concluded negotiation status.", () => {
    expect(
      createBuckets([2004, 2005, 2006])({
        negotiation_status: [
          { date: "2005", choice: "CONTRACT_SIGNED" },
          { choice: "CONTRACT_CANCELED" },
        ],
      } satisfies Partial<DealVersion2> as DealVersion2),
    ).toEqual([
      { count: 0, size: 0 },
      { count: 1, size: 0 },
      { count: 1, size: 0 },
    ])
  })
  test("a.2) Date is given on concluded and canceled negotiation status.", () => {
    expect(
      createBuckets([2004, 2005, 2006, 2007])({
        negotiation_status: [
          { date: "2005", choice: "CONTRACT_SIGNED" },
          { date: "2006", choice: "CONTRACT_CANCELED", current: true },
        ],
      } satisfies Partial<DealVersion2> as DealVersion2),
    ).toEqual([
      { count: 0, size: 0 },
      { count: 1, size: 0 },
      { count: 1, size: 0 },
      { count: 0, size: 0 },
    ])
  })
  test(
    "b) Substitution rule: " +
      "Date is missing on concluded negotiation status " +
      "and is substituted by earliest date on size under contract.",
    () => {
      expect(
        createBuckets([2004, 2005, 2006])({
          negotiation_status: [{ choice: "CONTRACT_SIGNED" }],
          contract_size: [
            { date: "2015", area: 70 },
            { date: "2005", area: 50 },
            { date: "2010", area: 100 },
          ],
        } satisfies Partial<DealVersion2> as DealVersion2),
      ).toEqual([
        { count: 0, size: 0 },
        { count: 1, size: 50 },
        { count: 1, size: 50 },
      ])
    },
  )
  test(
    "c) Exclusion rule: " +
      "Date is missing on concluded negotiation status and on size under contract " +
      "and marked as excluded.",
    () => {
      expect(
        createConcludedDealsOverTimeReducer([2004, 2005, 2006])(
          {
            excluded: { count: 0, size: 0 },
            buckets: [
              { size: 0, count: 0 },
              { size: 0, count: 0 },
              { size: 0, count: 0 },
            ],
          },
          {
            negotiation_status: [
              { choice: "CONTRACT_SIGNED" },
              { date: "2010", choice: "CONTRACT_CANCELED" },
            ],
            contract_size: [{ area: 50, current: true }, { area: 100 }],
          } satisfies Partial<DealVersion2> as DealVersion2,
        ),
      ).toEqual({
        excluded: { count: 1, size: 50 },
        buckets: [
          { size: 0, count: 0 },
          { size: 0, count: 0 },
          { size: 0, count: 0 },
        ],
      })
    },
  )
})

describe("Cumulated size under contract", () => {
  it("a) returns annual sizes for given date range.", () => {
    const deal = {
      negotiation_status: [{ choice: "CONTRACT_SIGNED", current: true }],
      contract_size: [
        { date: "2002", area: 20 },
        { date: "2004", area: 100, current: true },
      ],
    } satisfies Partial<DealVersion2> as DealVersion2
    const buckets = createBuckets([2000, 2001, 2002, 2003, 2004, 2005])(deal)
    expect(buckets).toEqual([
      { size: 0, count: 0 },
      { size: 0, count: 0 },
      { size: 20, count: 1 },
      { size: 20, count: 1 },
      { size: 100, count: 1 },
      { size: 100, count: 1 },
    ])
  })
  it("b) sets sizes to zero if current negotiation status is expired/failed/canceled.", () => {
    const deal = {
      negotiation_status: [
        { choice: "CONTRACT_SIGNED" },
        { date: "2004", choice: "CONTRACT_CANCELED", current: true },
      ],
      contract_size: [{ date: "2002", area: 20, current: true }],
    } satisfies Partial<DealVersion2> as DealVersion2
    const buckets = createBuckets([2000, 2001, 2002, 2003, 2004, 2005])(deal)
    expect(buckets).toEqual([
      { size: 0, count: 0 },
      { size: 0, count: 0 },
      { size: 20, count: 1 },
      { size: 20, count: 1 },
      { size: 20, count: 1 },
      { size: 0, count: 0 },
    ])
  })
  it(
    "c) substitutes contract size date (d_cs) with" +
      " negotiation status date (d_ns) if d_ns < d_cs",
    () => {
      const deal = {
        negotiation_status: [
          { date: "2001", choice: "CONTRACT_SIGNED", current: true },
        ],
        contract_size: [{ date: "2002", area: 20, current: true }],
      } satisfies Partial<DealVersion2> as DealVersion2
      const buckets = createBuckets([2000, 2001, 2002, 2003, 2004, 2005])(deal)
      expect(buckets).toEqual([
        { size: 0, count: 0 },
        { size: 20, count: 1 },
        { size: 20, count: 1 },
        { size: 20, count: 1 },
        { size: 20, count: 1 },
        { size: 20, count: 1 },
      ])
    },
  )
  it(
    "d) substitutes contract size date (d_cs) with" +
      " negotiation status date (d_ns) if not d_cs",
    () => {
      const deal = {
        negotiation_status: [
          { date: "2001", choice: "CONTRACT_SIGNED", current: true },
        ],
        contract_size: [{ area: 100, current: true }],
      } satisfies Partial<DealVersion2> as DealVersion2
      const buckets = createBuckets([2000, 2001, 2002, 2003, 2004, 2005])(deal)
      expect(buckets).toEqual([
        { size: 0, count: 0 },
        { size: 100, count: 1 },
        { size: 100, count: 1 },
        { size: 100, count: 1 },
        { size: 100, count: 1 },
        { size: 100, count: 1 },
      ])
    },
  )
})

describe("createYearSizeMap", () => {
  it("returns empty map if no dates are given", () => {
    expect(
      createYearSizeMap({} satisfies Partial<DealVersion2> as DealVersion2),
    ).toEqual({})
    expect(
      createYearSizeMap({
        contract_size: [] as ContractSizeItem[],
      } satisfies Partial<DealVersion2> as DealVersion2),
    ).toEqual({})
    expect(
      createYearSizeMap({
        contract_size: [{ area: 20 }, { area: 50, current: true }],
      } satisfies Partial<DealVersion2> as DealVersion2),
    ).toEqual({})
  })

  it("returns map from all dated contract sizes", () => {
    const deal = {
      contract_size: [
        { area: 20, date: "2020" },
        { area: 10, date: "2015" },
        { area: 100 },
        { area: 50, date: "2022", current: true },
      ],
    } satisfies Partial<DealVersion2> as DealVersion2

    expect(createYearSizeMap(deal)).toEqual({
      2015: 10,
      2020: 20,
      2022: 50,
    })
  })

  describe("multiple contract sizes have same date", () => {
    it("takes item flagged as current", () => {
      const deal = {
        contract_size: [
          { area: 10, date: "2020" },
          { area: 20, date: "2020", current: true },
          { area: 50, date: "2020" },
        ],
      } satisfies Partial<DealVersion2> as DealVersion2
      const yearSizeMap = createYearSizeMap(deal)

      expect(yearSizeMap).toEqual({ 2020: 20 })
    })

    it("takes last item in list", () => {
      const deal = {
        contract_size: [
          { area: 10, date: "2020" },
          { area: 20, date: "2020" },
          { area: 50, date: "2020" },
        ],
      } satisfies Partial<DealVersion2> as DealVersion2
      const yearSizeMap = createYearSizeMap(deal)

      expect(yearSizeMap).toEqual({ 2020: 50 })
    })
  })
})
