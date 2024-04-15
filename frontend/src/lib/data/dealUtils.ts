import * as R from "ramda"

import {
  getCurrent,
  getFirstByDate,
  getLastByDate,
  isDated,
  parseDate,
} from "$lib/data/itemUtils"
import type { IsCurrent } from "$lib/data/itemUtils"
import type { ContractSizeItem, NegotiationStatusItem } from "$lib/types/deal"
import { NegotiationStatus } from "$lib/types/deal"
import type { DealVersion2 } from "$lib/types/newtypes"

export const isConcludedItem: (item: NegotiationStatusItem) => boolean =
  R.propSatisfies(
    R.includes(R.__, [
      NegotiationStatus.ORAL_AGREEMENT,
      NegotiationStatus.CONTRACT_SIGNED,
    ]),
    "choice",
  )

export const isCanceledItem: (item: NegotiationStatusItem) => boolean = R.propSatisfies(
  R.includes(R.__, [
    NegotiationStatus.CONTRACT_CANCELED,
    NegotiationStatus.CONTRACT_EXPIRED,
    NegotiationStatus.NEGOTIATIONS_FAILED,
  ]),
  "choice",
)

export const hasBeenConcluded: (deal: DealVersion2) => boolean = R.pipe(
  R.propOr<NegotiationStatusItem[]>([], "negotiation_status"),
  R.any(isConcludedItem),
)

export const isConcluded: (deal: DealVersion2) => boolean = R.propSatisfies(
  R.includes(R.__, [
    NegotiationStatus.ORAL_AGREEMENT,
    NegotiationStatus.CONTRACT_SIGNED,
    NegotiationStatus.CHANGE_OF_OWNERSHIP,
  ]),
  "current_negotiation_status",
)

export const getCanceledDate: (deal: DealVersion2) => number | undefined = R.pipe<
  [DealVersion2],
  NegotiationStatusItem[],
  NegotiationStatusItem[],
  NegotiationStatusItem | undefined,
  number | undefined
>(
  R.propOr([], "negotiation_status"),
  R.filter(isCanceledItem),
  getLastByDate,
  R.unless(R.isNil, R.pipe(R.prop("date"), parseDate)),
)

export const hasConcludedDate = (deal: DealVersion2): boolean => {
  const negStats: NegotiationStatusItem[] = R.propOr([], "negotiation_status", deal)
  const cSizes: ContractSizeItem[] = R.propOr([], "contract_size", deal)
  return R.or(
    R.pipe(R.filter(isConcludedItem), R.any(isDated))(negStats),
    R.any(isDated, cSizes),
  )
}

export const getConcludedDate = (deal: DealVersion2): number => {
  const negStats: NegotiationStatusItem[] = R.propOr([], "negotiation_status", deal)
  const cSizes: ContractSizeItem[] = R.propOr([], "contract_size", deal)
  const firstConcluded: NegotiationStatusItem | undefined = R.pipe(
    R.filter(isConcludedItem) as (
      items: NegotiationStatusItem[],
    ) => NegotiationStatusItem[],
    getFirstByDate,
  )(negStats)
  const firstSizeItem = getFirstByDate(cSizes)

  if (firstConcluded) {
    return R.pipe(R.prop("date"), parseDate)(firstConcluded)
  } else {
    return R.pipe(R.prop("date"), parseDate)(firstSizeItem)
  }
}

export const getConcludedRange = (deal: DealVersion2): [number, number | undefined] => {
  return [getConcludedDate(deal), getCanceledDate(deal)]
}

export const getInitialSize = (deal: DealVersion2): number => {
  const cSizes: ContractSizeItem[] = R.propOr([], "contract_size", deal)
  const firstSizeItem = getFirstByDate(cSizes)
  if (firstSizeItem) {
    return R.propOr(0, "area", firstSizeItem)
  }
  const currentContractSizeItem = getCurrent(cSizes)
  return R.propOr(0, "area", currentContractSizeItem)
}

export const getCurrentSize: (deal: DealVersion2) => number = R.pipe<
  [DealVersion2],
  ContractSizeItem[],
  IsCurrent<ContractSizeItem> | undefined,
  number
>(R.propOr([], "contract_size"), getCurrent, R.propOr(0, "area"))
