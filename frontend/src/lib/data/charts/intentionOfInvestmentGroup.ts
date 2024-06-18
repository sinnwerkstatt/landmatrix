import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS, type DealReducer } from "$lib/data/createChartData"
import { IntentionOfInvestmentGroup, type IoIGroupMap } from "$lib/types/data"

export const INTENTION_OF_INVESTMENT_GROUP_COLORS: {
  [key in IntentionOfInvestmentGroup]: string
} = {
  [IntentionOfInvestmentGroup.AGRICULTURE]: COLORS.ORANGE,
  [IntentionOfInvestmentGroup.FORESTRY]: COLORS.ORANGE_DARK,
  [IntentionOfInvestmentGroup.RENEWABLE_ENERGY]: COLORS.ORANGE_LIGHT,
  [IntentionOfInvestmentGroup.OTHER]: COLORS.BLACK,
}

export const createIoIGroupReducer: (
  groupMap: IoIGroupMap,
) => DealReducer<IntentionOfInvestmentGroup> =
  (groupMap: IoIGroupMap) => (bucketMap, deal) => {
    const intentions = deal.current_intention_of_investment ?? []

    const intentionGroups = intentions.map(intention => groupMap[intention])
    const uniqueIntentionGroups = [...new Set(intentionGroups)].filter(
      (x): x is IntentionOfInvestmentGroup => x !== undefined,
    )
    return uniqueIntentionGroups.reduce(
      createBucketMapReducer(deal.deal_size ?? 0),
      bucketMap,
    )
  }
