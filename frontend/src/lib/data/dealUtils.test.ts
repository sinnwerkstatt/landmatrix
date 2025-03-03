import { getConcludedDate, hasConcludedDate } from "$lib/data/dealUtils"
import type { ContractSizeItem, NegotiationStatusItem } from "$lib/data/dealUtils"
import type { DealVersion } from "$lib/types/data"

describe("getConcludedDate", () => {
  it("returns year on concluded negotiation status", () => {
    const deal = {
      negotiation_status: [{ choice: "CONTRACT_SIGNED", date: "2010", current: true }],
    } satisfies Partial<DealVersion> as DealVersion
    expect(getConcludedDate(deal)).toBe(2010)
  })
  it("returns earliest year of contract sizes", () => {
    const deal = {
      negotiation_status: [{ choice: "CONTRACT_SIGNED", current: true }],
      contract_size: [{ area: 20, date: "2010" }],
    } satisfies Partial<DealVersion> as DealVersion
    expect(getConcludedDate(deal)).toBe(2010)
  })
})

describe("hasConcludedDate", () => {
  it("returns false if no negotiation status nor contract size recorded", () => {
    expect(
      hasConcludedDate({} satisfies Partial<DealVersion> as DealVersion),
    ).toBeFalsy()
    expect(
      hasConcludedDate({
        negotiation_status: [] as NegotiationStatusItem[],
        contract_size: [] as ContractSizeItem[],
      } satisfies Partial<DealVersion> as DealVersion),
    ).toBeFalsy()
  })
  it("returns false if neither negotiation status nor contract sizes have date", () => {
    const deal = {
      negotiation_status: [
        { choice: "ORAL_AGREEMENT" },
        { choice: "CONTRACT_SIGNED", current: true },
      ],
      contract_size: [{ area: 10 }, { area: 20, current: true }],
    } satisfies Partial<DealVersion> as DealVersion
    expect(hasConcludedDate(deal)).toBeFalsy()
  })
  it("returns true if any date on concluded negotiation status", () => {
    const deal = {
      negotiation_status: [
        { choice: "ORAL_AGREEMENT" },
        { choice: "CONTRACT_SIGNED", date: "2010", current: true },
      ],
    } satisfies Partial<DealVersion> as DealVersion
    expect(hasConcludedDate(deal)).toBeTruthy()
  })
  it("returns true if concluded and any date on contract sizes", () => {
    const deal = {
      negotiation_status: [
        { choice: "ORAL_AGREEMENT" },
        { choice: "CONTRACT_SIGNED", current: true },
      ],
      contract_size: [{ area: 10 }, { area: 20, date: "2010", current: true }],
    } satisfies Partial<DealVersion> as DealVersion
    expect(hasConcludedDate(deal)).toBeTruthy()
  })
})
