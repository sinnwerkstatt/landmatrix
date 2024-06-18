import { createBucketMapReducer } from "$lib/data/buckets"
import type { DealReducer } from "$lib/data/createChartData"
import { COLORS } from "$lib/data/createChartData"
import { NegotiationStatusGroup, type NegStatGroupMap } from "$lib/types/data"

export const NEGOTIATION_STATUS_GROUP_COLORS: {
  [key in NegotiationStatusGroup]: string
} = {
  [NegotiationStatusGroup.INTENDED]: COLORS.ORANGE_LIGHTER,
  [NegotiationStatusGroup.CONCLUDED]: COLORS.ORANGE,
  [NegotiationStatusGroup.FAILED]: COLORS.ORANGE_DARK,
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: COLORS.BROWN,
}

export const getNegotiationStatusGroupColor = (
  negotiationStatusGroup: NegotiationStatusGroup,
) => NEGOTIATION_STATUS_GROUP_COLORS[negotiationStatusGroup]

export const createNegotiationStatusGroupReducer: (
  groupMap: NegStatGroupMap,
) => DealReducer<NegotiationStatusGroup> = groupMap => (bucketMap, deal) => {
  const negStatus = deal.current_negotiation_status

  if (negStatus)
    return createBucketMapReducer(deal.deal_size ?? 0)(bucketMap, groupMap[negStatus])

  return bucketMap
}
