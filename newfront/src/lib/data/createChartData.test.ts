import { createBucketMap } from "$lib/data/buckets";
import { agricultureIntentionReducer } from "$lib/data/charts/agricultureIntention";
import { intentionOfInvestmentGroupReducer } from "$lib/data/charts/intentionOfInvestmentGroup";
import type { Deal } from "$lib/types/deal";
import { IntentionOfInvestment, IntentionOfInvestmentGroup } from "$lib/types/deal";

describe("Dynamics Overview Logic", () => {
  test("intentionOfInvestmentReducer", () => {
    const deals = [
      {
        current_intention_of_investment: [
          IntentionOfInvestment.CARBON,
          IntentionOfInvestment.MINING,
          IntentionOfInvestment.BIOFUELS,
        ],
        deal_size: 500,
      },
      {
        current_intention_of_investment: [IntentionOfInvestment.BIOFUELS],
        deal_size: undefined,
      },
      {
        current_intention_of_investment: [IntentionOfInvestment.CARBON],
        deal_size: 50,
      },
    ] as Deal[];

    const emptyIntentionBuckets = createBucketMap(Object.values(IntentionOfInvestment));

    const filledIntentionBuckets = deals.reduce(
      agricultureIntentionReducer,
      emptyIntentionBuckets
    );

    expect(filledIntentionBuckets).toMatchObject({
      [IntentionOfInvestment.CARBON]: { count: 2, size: 550 },
      [IntentionOfInvestment.BIOFUELS]: { count: 2, size: 500 },
      [IntentionOfInvestment.MINING]: { count: 1, size: 500 },
      // All the other intention buckets are empty, e.g.
      [IntentionOfInvestment.OTHER]: { count: 0, size: 0 },
    });
  });

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
