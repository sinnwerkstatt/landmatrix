import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS } from "$lib/data/createChartData"
import type { DealReducer } from "$lib/data/createChartData"
import { ProduceGroup } from "$lib/types/data"

type ProduceGroupMap = { [key in ProduceGroup]: string }

const PRODUCE_GROUP_COLORS: ProduceGroupMap = {
  [ProduceGroup.CROPS]: COLORS.ORANGE,
  [ProduceGroup.ANIMALS]: COLORS.ORANGE_DARK,
  [ProduceGroup.MINERAL_RESOURCES]: COLORS.BLACK,
}

export const getProduceGroupColor = (produceGroup: ProduceGroup) =>
  PRODUCE_GROUP_COLORS[produceGroup]

export const produceGroupReducer: DealReducer<ProduceGroup> = (bucketMap, deal) => {
  const groups: ProduceGroup[] = []

  if (deal.current_crops?.length) groups.push(ProduceGroup.CROPS)
  if (deal.current_animals?.length) groups.push(ProduceGroup.ANIMALS)
  if (deal.current_mineral_resources?.length)
    groups.push(ProduceGroup.MINERAL_RESOURCES)

  const bucketMapReducer = createBucketMapReducer<ProduceGroup>(deal.deal_size ?? 0)
  return groups.reduce(bucketMapReducer, bucketMap)
}
