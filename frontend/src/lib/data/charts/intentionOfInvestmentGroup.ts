import { get } from "svelte/store"

import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS } from "$lib/data/createChartData"
import type { DealReducer } from "$lib/data/createChartData"
import { fieldChoices, getFieldChoicesGroup } from "$lib/stores"
import { IntentionOfInvestmentGroup, type DealVersion2 } from "$lib/types/data"

export const INTENTION_OF_INVESTMENT_GROUP_COLORS: {
  [key in IntentionOfInvestmentGroup]: string
} = {
  [IntentionOfInvestmentGroup.AGRICULTURE]: COLORS.ORANGE,
  [IntentionOfInvestmentGroup.FORESTRY]: COLORS.ORANGE_DARK,
  [IntentionOfInvestmentGroup.RENEWABLE_ENERGY]: COLORS.ORANGE_LIGHT,
  [IntentionOfInvestmentGroup.OTHER]: COLORS.BLACK,
}

export const intentionOfInvestmentGroupReducer: DealReducer<
  IntentionOfInvestmentGroup
> = (
  bucketMap: BucketMap<IntentionOfInvestmentGroup>,
  deal: DealVersion2,
): BucketMap<IntentionOfInvestmentGroup> => {
  const intentions = deal.current_intention_of_investment ?? []

  const getGroup = getFieldChoicesGroup(
    get(fieldChoices)["deal"]["intention_of_investment"],
  )
  const intentionGroups = intentions.map(intention => getGroup(intention))
  const uniqueIntentionGroups = [...new Set(intentionGroups)].filter(
    (x): x is IntentionOfInvestmentGroup => x !== undefined,
  )
  return uniqueIntentionGroups.reduce(
    createBucketMapReducer(deal.deal_size ?? 0),
    bucketMap,
  )
}
