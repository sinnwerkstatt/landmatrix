import { createBucketMapReducer } from "$lib/data/buckets"
import type { IoIGroupMap } from "$lib/data/charts/intentionOfInvestmentGroup"
import type { DealReducer } from "$lib/data/createChartData"
import { IntentionOfInvestmentGroup, type IntentionOfInvestment } from "$lib/types/data"

export const createAgricultureIntentionReducer: (
  groupMap: IoIGroupMap,
) => DealReducer<IntentionOfInvestment> = groupMap => (bucketMap, deal) => {
  const intentions = deal.current_intention_of_investment ?? []

  const agricultureIntentions: IntentionOfInvestment[] = intentions.filter(
    intention => groupMap[intention] === IntentionOfInvestmentGroup.AGRICULTURE,
  )
  return agricultureIntentions.reduce(
    createBucketMapReducer(deal.deal_size ?? 0),
    bucketMap,
  )
}
