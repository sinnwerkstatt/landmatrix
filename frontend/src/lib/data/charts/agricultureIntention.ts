import { get } from "svelte/store"

import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { fieldChoices, getFieldChoicesGroup } from "$lib/stores"
import { IntentionOfInvestmentGroup, type DealVersion2 } from "$lib/types/data"

export const agricultureIntentionReducer = (
  bucketMap: BucketMap,
  deal: DealVersion2,
): BucketMap => {
  const intentions = deal.current_intention_of_investment ?? []
  const getGroup = getFieldChoicesGroup(
    get(fieldChoices)["deal"]["intention_of_investment"],
  )
  const agricultureIntentions = intentions.filter(
    intention => getGroup(intention) === IntentionOfInvestmentGroup.AGRICULTURE,
  )
  return agricultureIntentions.reduce(
    createBucketMapReducer(deal.deal_size ?? 0),
    bucketMap,
  )
}
