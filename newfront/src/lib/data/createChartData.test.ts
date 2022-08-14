import { createBucketMap } from "$lib/data/buckets";
import { intentionOfInvestmentGroupReducer } from "$lib/data/charts/intentionOfInvestmentGroup";
import type { Deal } from "$lib/types/deal";
import { IntentionOfInvestment, IntentionOfInvestmentGroup } from "$lib/types/deal";

describe("Dynamics Overview Logic", () => {
  test("intentionOfInvestmentGroupReducer", () => {
    const deals = [
      {
        current_intention_of_investment: [
          IntentionOfInvestment.CARBON,
          IntentionOfInvestment.TIMBER_PLANTATION,
          IntentionOfInvestment.FOREST_LOGGING,
        ],
        deal_size: 500,
      },
      {
        current_intention_of_investment: [
          IntentionOfInvestment.BIOFUELS,
          IntentionOfInvestment.FODDER,
        ],
        deal_size: undefined,
      },
      {
        current_intention_of_investment: [
          IntentionOfInvestment.CARBON,
          IntentionOfInvestment.FORESTRY_UNSPECIFIED,
        ],
        deal_size: 50,
      },
    ] as Deal[];

    const emptyIntentionGroupBuckets = createBucketMap(
      Object.values(IntentionOfInvestmentGroup)
    );

    const filledIntentionGroupBuckets = deals.reduce(
      intentionOfInvestmentGroupReducer,
      emptyIntentionGroupBuckets
    );

    expect(filledIntentionGroupBuckets).toMatchObject({
      [IntentionOfInvestmentGroup.FORESTRY]: { count: 2, size: 550 },
      [IntentionOfInvestmentGroup.AGRICULTURE]: { count: 1, size: 0 },
      [IntentionOfInvestmentGroup.OTHER]: { count: 0, size: 0 },
    });
  });
});
