import { intention_of_investment_group_choices } from "$lib/choices"
import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS, createChartData } from "$lib/data/createChartData"
import type { DealReducer } from "$lib/data/createChartData"
import type { Deal } from "$lib/types/deal"
import {
  INTENTION_OF_INVESTMENT_GROUP_MAP,
  IntentionOfInvestmentGroup,
} from "$lib/types/deal"

const INTENTION_OF_INVESTMENT_GROUP_COLORS: {
  [key in IntentionOfInvestmentGroup]: string
} = {
  [IntentionOfInvestmentGroup.AGRICULTURE]: COLORS.ORANGE,
  [IntentionOfInvestmentGroup.FORESTRY]: COLORS.ORANGE_DARK,
  [IntentionOfInvestmentGroup.OTHER]: COLORS.BLACK,
}

const getIntentionOfInvestmentGroupLabel = (
  intentionGroup: IntentionOfInvestmentGroup,
) => intention_of_investment_group_choices[intentionGroup]

const getIntentionOfInvestmentGroupColor = (
  intentionGroup: IntentionOfInvestmentGroup,
) => INTENTION_OF_INVESTMENT_GROUP_COLORS[intentionGroup]

export const intentionOfInvestmentGroupReducer: DealReducer<
  IntentionOfInvestmentGroup
> = (
  bucketMap: BucketMap<IntentionOfInvestmentGroup>,
  deal: Deal,
): BucketMap<IntentionOfInvestmentGroup> => {
  const intentions = deal.current_intention_of_investment ?? []
  const intentionGroups = intentions.map(
    intention => INTENTION_OF_INVESTMENT_GROUP_MAP[intention],
  )
  const uniqueIntentionGroups = [...new Set(intentionGroups)]
  return uniqueIntentionGroups.reduce(createBucketMapReducer(deal.deal_size), bucketMap)
}

export const createIntentionOfInvestmentGroupChartData =
  createChartData<IntentionOfInvestmentGroup>(
    intentionOfInvestmentGroupReducer,
    Object.values(IntentionOfInvestmentGroup),
    getIntentionOfInvestmentGroupLabel,
    getIntentionOfInvestmentGroupColor,
  )
