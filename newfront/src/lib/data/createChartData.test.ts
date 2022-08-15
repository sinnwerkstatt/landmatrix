import { createBucketMapReducer } from "$lib/data/buckets";
import { createChartData } from "$lib/data/createChartData";
import type { Deal } from "$lib/types/deal";

test("createChartData", () => {
  const deals = [
    { deal_size: -10 },
    { deal_size: -1 },
    { deal_size: 1 },
    { deal_size: 100 },
    { deal_size: undefined },
    { deal_size: -100 },
    { deal_size: 0 },
  ] as Deal[];

  type BucketKeys = "negative" | "positive" | "zero";
  const bucketKeys: BucketKeys[] = ["negative", "positive", "zero"];
  const createDealSizeSignData = createChartData<BucketKeys>(
    (bucketMap, deal) => {
      const reducer = createBucketMapReducer(deal.deal_size);

      if (deal.deal_size !== undefined)
        if (deal.deal_size < 0) return ["negative"].reduce(reducer, bucketMap);
        else if (deal.deal_size > 0) return ["positive"].reduce(reducer, bucketMap);
        else return ["zero"].reduce(reducer, bucketMap);

      return bucketMap;
    },
    bucketKeys,
    (key, index) => `Label ${key}`,
    (key, index) => `Color ${key}`
  );

  expect(createDealSizeSignData(deals, "count")).toEqual({
    labels: ["Label negative", "Label positive", "Label zero"],
    datasets: [
      {
        data: [3, 2, 1],
        backgroundColor: ["Color negative", "Color positive", "Color zero"],
      },
    ],
  });
  expect(createDealSizeSignData(deals, "size")).toEqual({
    labels: ["Label positive", "Label zero", "Label negative"],
    datasets: [
      {
        data: [101, 0, -111],
        backgroundColor: ["Color positive", "Color zero", "Color negative"],
      },
    ],
  });
});
