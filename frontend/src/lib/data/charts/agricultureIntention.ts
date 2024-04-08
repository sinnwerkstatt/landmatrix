import { get } from "svelte/store"

import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { createChartData } from "$lib/data/createChartData"
import { intentionOfInvestmentMap } from "$lib/stores/maps"
import type { Deal } from "$lib/types/deal"
import {
  AgricultureIoI,
  INTENTION_OF_INVESTMENT_GROUP_MAP,
  IntentionOfInvestmentGroup,
} from "$lib/types/deal"

const getAgricultureIntentionLabel = (intention: AgricultureIoI) =>
  get(intentionOfInvestmentMap)[intention]

export const agricultureIntentionReducer = (
  bucketMap: BucketMap<AgricultureIoI>,
  deal: Deal,
): BucketMap<AgricultureIoI> => {
  const intentions = deal.current_intention_of_investment ?? []
  const agricultureIntentions = intentions.filter(
    (intention): intention is AgricultureIoI =>
      INTENTION_OF_INVESTMENT_GROUP_MAP[intention] ===
      IntentionOfInvestmentGroup.AGRICULTURE,
  )
  return agricultureIntentions.reduce(createBucketMapReducer(deal.deal_size), bucketMap)
}

export const createAgricultureIntentionChartData = createChartData<AgricultureIoI>(
  agricultureIntentionReducer,
  Object.values(AgricultureIoI),
  getAgricultureIntentionLabel,
  (_, index, array) => {
    const alphaValue = 1 - index / array.length
    return `rgba(252,148,31,${alphaValue})`
  },
)
