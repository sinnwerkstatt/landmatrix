import { get } from "svelte/store"

import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS, createChartData } from "$lib/data/createChartData"
import type { DealReducer } from "$lib/data/createChartData"
import { fieldChoices, getFieldChoicesLabel } from "$lib/stores"
import { NegotiationStatusGroup } from "$lib/types/data"

export const NEGOTIATION_STATUS_GROUP_COLORS: {
  [key in NegotiationStatusGroup]: string
} = {
  [NegotiationStatusGroup.INTENDED]: COLORS.ORANGE_LIGHTER,
  [NegotiationStatusGroup.CONCLUDED]: COLORS.ORANGE,
  [NegotiationStatusGroup.FAILED]: COLORS.ORANGE_DARK,
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: COLORS.BROWN,
}

const getNegotiationStatusGroupColor = (negotiationStatusGroup: NegotiationStatusGroup) =>
  NEGOTIATION_STATUS_GROUP_COLORS[negotiationStatusGroup]

export const negotiationStatusGroupReducer: DealReducer<NegotiationStatusGroup> = (
  bucketMap,
  deal,
): BucketMap<NegotiationStatusGroup> => {
  const negStatus = deal.current_negotiation_status

  const getLabel = getFieldChoicesLabel(
    get(fieldChoices)["deal"]["negotiation_status_group"],
  )
  if (negStatus)
    return createBucketMapReducer(deal.deal_size ?? 0)(bucketMap, getLabel(negStatus)!)

  return bucketMap
}

export const createNegotiationStatusChartData = createChartData(
  negotiationStatusGroupReducer,
  Object.values(NegotiationStatusGroup),
  getFieldChoicesLabel(get(fieldChoices)["deal"]["negotiation_status_group"]) as (
    key: string,
  ) => NegotiationStatusGroup,
  getNegotiationStatusGroupColor,
)
