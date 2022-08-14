import { agriculture_investment_choices } from "$lib/choices";
import type { BucketMap } from "$lib/data/buckets";
import { createBucketMapReducer } from "$lib/data/buckets";
import { createChartData } from "$lib/data/createChartData";
import type { Deal } from "$lib/types/deal";
import {
  INTENTION_OF_INVESTMENT_GROUP_MAP,
  IntentionOfInvestmentGroup,
} from "$lib/types/deal";

type AgricultureIntention = keyof typeof agriculture_investment_choices;

const getAgricultureIntentionLabel = (intention: AgricultureIntention) =>
  agriculture_investment_choices[intention];

export const agricultureIntentionReducer = (
  bucketMap: BucketMap<AgricultureIntention>,
  deal: Deal
): BucketMap<AgricultureIntention> => {
  const intentions = deal.current_intention_of_investment ?? [];
  const agricultureIntentions = intentions.filter(
    (intention): intention is AgricultureIntention =>
      INTENTION_OF_INVESTMENT_GROUP_MAP[intention] ===
      IntentionOfInvestmentGroup.AGRICULTURE
  );
  return agricultureIntentions.reduce(
    createBucketMapReducer(deal.deal_size),
    bucketMap
  );
};

export const createAgricultureIntentionChartData =
  createChartData<AgricultureIntention>(
    agricultureIntentionReducer,
    Object.keys(agriculture_investment_choices) as AgricultureIntention[],
    getAgricultureIntentionLabel,
    (_, index, array) => {
      const alphaValue = 1 - index / array.length;
      return `rgba(252,148,31,${alphaValue})`;
    }
  );
