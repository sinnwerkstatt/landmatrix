import { getConcludedDate, hasConcludedDate } from "$lib/data/dealUtils"
import { NegotiationStatus } from "$lib/types/deal"
import type { ContractSizeItem, Deal, NegotiationStatusItem } from "$lib/types/deal"

describe("getConcludedDate", () => {
  it("returns year on concluded negotiation status", () => {
    const deal = {
      negotiation_status: [
        { choice: NegotiationStatus.CONTRACT_SIGNED, date: "2010", current: true },
      ],
    } as Deal
    expect(getConcludedDate(deal)).toBe(2010)
  })
  it("returns earliest year of contract sizes", () => {
    const deal = {
      negotiation_status: [
        { choice: NegotiationStatus.CONTRACT_SIGNED, current: true },
      ],
      contract_size: [{ area: 20, date: "2010" }],
    } as Deal
    expect(getConcludedDate(deal)).toBe(2010)
  })
})

describe("hasConcludedDate", () => {
  it("returns false if no negotiation status nor contract size recorded", () => {
    expect(hasConcludedDate({} as Deal)).toBeFalsy()
    expect(
      hasConcludedDate({
        negotiation_status: [] as NegotiationStatusItem[],
        contract_size: [] as ContractSizeItem[],
      } as Deal),
    ).toBeFalsy()
  })
  it("returns false if neither negotiation status nor contract sizes have date", () => {
    const deal = {
      negotiation_status: [
        { choice: NegotiationStatus.ORAL_AGREEMENT },
        { choice: NegotiationStatus.CONTRACT_SIGNED, current: true },
      ],
      contract_size: [{ area: 10 }, { area: 20, current: true }],
    } as Deal
    expect(hasConcludedDate(deal)).toBeFalsy()
  })
  it("returns true if any date on concluded negotiation status", () => {
    const deal = {
      negotiation_status: [
        { choice: NegotiationStatus.ORAL_AGREEMENT },
        { choice: NegotiationStatus.CONTRACT_SIGNED, date: "2010", current: true },
      ],
    } as Deal
    expect(hasConcludedDate(deal)).toBeTruthy()
  })
  it("returns true if concluded and any date on contract sizes", () => {
    const deal = {
      negotiation_status: [
        { choice: NegotiationStatus.ORAL_AGREEMENT },
        { choice: NegotiationStatus.CONTRACT_SIGNED, current: true },
      ],
      contract_size: [{ area: 10 }, { area: 20, date: "2010", current: true }],
    } as Deal
    expect(hasConcludedDate(deal)).toBeTruthy()
  })
})
