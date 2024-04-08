import { get } from "svelte/store"

import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS, createChartData } from "$lib/data/createChartData"
import type { DealReducer } from "$lib/data/createChartData"
import { negotiationStatusGroupMap } from "$lib/stores/maps"
import { NEGOTIATION_STATUS_GROUP_MAP, NegotiationStatusGroup } from "$lib/types/deal"

export const NEGOTIATION_STATUS_GROUP_COLORS: {
  [key in NegotiationStatusGroup]: string
} = {
  [NegotiationStatusGroup.INTENDED]: COLORS.ORANGE_LIGHTER,
  [NegotiationStatusGroup.CONCLUDED]: COLORS.ORANGE,
  [NegotiationStatusGroup.FAILED]: COLORS.ORANGE_DARK,
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: COLORS.BROWN,
}

const getNegotiationStatusGroupLabel = (
  negotiationStatusGroup: NegotiationStatusGroup,
) => get(negotiationStatusGroupMap)[negotiationStatusGroup]

const getNegotiationStatusGroupColor = (
  negotiationStatusGroup: NegotiationStatusGroup,
) => NEGOTIATION_STATUS_GROUP_COLORS[negotiationStatusGroup]

export const negotiationStatusGroupReducer: DealReducer<NegotiationStatusGroup> = (
  bucketMap,
  deal,
): BucketMap<NegotiationStatusGroup> => {
  const negStatus = deal.current_negotiation_status

  if (negStatus)
    return createBucketMapReducer(deal.deal_size)(
      bucketMap,
      NEGOTIATION_STATUS_GROUP_MAP[negStatus],
    )

  return bucketMap
}

export const createNegotiationStatusChartData = createChartData(
  negotiationStatusGroupReducer,
  Object.values(NegotiationStatusGroup),
  getNegotiationStatusGroupLabel,
  getNegotiationStatusGroupColor,
)
