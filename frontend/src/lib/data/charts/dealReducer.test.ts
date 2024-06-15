import { createEmptyBuckets } from "$lib/data/buckets"
import { agricultureIntentionReducer } from "$lib/data/charts/agricultureIntention"
import { implementationStatusReducer } from "$lib/data/charts/implementationStatus"
import { intentionOfInvestmentGroupReducer } from "$lib/data/charts/intentionOfInvestmentGroup"
import { negotiationStatusGroupReducer } from "$lib/data/charts/negotiationStatusGroup"
import { produceGroupReducer } from "$lib/data/charts/produceGroup"
import {
  IntentionOfInvestmentGroup,
  NegotiationStatusGroup,
  ProduceGroup,
  type DealVersion2,
  type ImplementationStatus,
  type IntentionOfInvestment,
} from "$lib/types/data"

describe("Intention of Investment Group", () => {
  test("Multiple intentions of same group per deal are counted as 1", () => {
    const deals = [
      {
        current_intention_of_investment: [
          "CARBON",
          "TIMBER_PLANTATION",
          "FOREST_LOGGING",
          "SOLAR_PARK",
          "BIOFUELS",
        ],
        deal_size: 500,
      } satisfies Partial<DealVersion2>,
      {
        current_intention_of_investment: [
          "MINING",
          "CONVERSATION",
          "BIOFUELS",
          "WIND_FARM",
        ],
        deal_size: 100,
      } satisfies Partial<DealVersion2>,
      // I don't understand this type error but need to convert to unknown
    ] as unknown as DealVersion2[]

    const bucketMap = deals.reduce(
      intentionOfInvestmentGroupReducer,
      createEmptyBuckets(Object.values(IntentionOfInvestmentGroup)),
    )

    expect(bucketMap).toEqual({
      [IntentionOfInvestmentGroup.FORESTRY]: { count: 1, size: 500 },
      [IntentionOfInvestmentGroup.AGRICULTURE]: { count: 2, size: 600 },
      [IntentionOfInvestmentGroup.RENEWABLE_ENERGY]: { count: 2, size: 600 },
      [IntentionOfInvestmentGroup.OTHER]: { count: 1, size: 100 },
    })
  })
})

describe("Agriculture Intention of Investment", () => {
  test("Only count agriculture intentions", () => {
    const deals = [
      {
        current_intention_of_investment: ["CARBON", "FOREST_LOGGING", "BIOFUELS"],
        deal_size: 500,
      },
      {
        current_intention_of_investment: ["MINING", "BIOFUELS", "FOOD_CROPS"],
        deal_size: 100,
      },
    ] satisfies Partial<DealVersion2>[]

    const bucketMap = deals.reduce(
      agricultureIntentionReducer,
      createEmptyBuckets([
        "BIOFUELS",
        "BIOMASS_ENERGY_GENERATION",
        "FOOD_CROPS",
        "FODDER",
        "LIVESTOCK",
        "NON_FOOD_AGRICULTURE",
        "AGRICULTURE_UNSPECIFIED",
      ] satisfies IntentionOfInvestment[] as IntentionOfInvestment[]),
    )

    expect(bucketMap).toEqual({
      BIOFUELS: { count: 2, size: 600 },
      BIOMASS_ENERGY_GENERATION: { count: 0, size: 0 },
      FOOD_CROPS: { count: 1, size: 100 },
      FODDER: { count: 0, size: 0 },
      LIVESTOCK: { count: 0, size: 0 },
      NON_FOOD_AGRICULTURE: { count: 0, size: 0 },
      AGRICULTURE_UNSPECIFIED: { count: 0, size: 0 },
    })
  })
})

describe("Produce Group", () => {
  test("Count non empty existing fields", () => {
    const deals: DealVersion2[] = [
      {
        current_animals: ["cows", "bees"] as readonly string[],
        current_crops: ["corn"] as readonly string[],
        deal_size: 500,
      } satisfies Partial<DealVersion2> as DealVersion2,
      {
        current_animals: ["sloths"] as readonly string[],
        current_mineral_resources: [] as readonly string[],
        deal_size: 100,
      } satisfies Partial<DealVersion2> as DealVersion2,
    ]

    const bucketMap = deals.reduce(
      produceGroupReducer,
      createEmptyBuckets(Object.values(ProduceGroup)),
    )

    expect(bucketMap).toEqual({
      [ProduceGroup.ANIMALS]: { count: 2, size: 600 },
      [ProduceGroup.CROPS]: { count: 1, size: 500 },
      [ProduceGroup.MINERAL_RESOURCES]: { count: 0, size: 0 },
    })
  })
})

describe("Negotiation Status Group", () => {
  test("Existing negotiation status is mapped to group", () => {
    const deals = [
      {
        current_negotiation_status: "CONTRACT_SIGNED",
        deal_size: 500,
      },
      {
        current_negotiation_status: "CONTRACT_EXPIRED",
        deal_size: 100,
      },
      {
        // current_implementation_status: undefined,
        deal_size: 1_000_000_000_000_000_000,
      },
    ] satisfies Partial<DealVersion2>[] as DealVersion2[]

    const bucketMap = deals.reduce(
      negotiationStatusGroupReducer,
      createEmptyBuckets(Object.values(NegotiationStatusGroup)),
    )

    expect(bucketMap).toEqual({
      [NegotiationStatusGroup.CONCLUDED]: { count: 1, size: 500 },
      [NegotiationStatusGroup.CONTRACT_EXPIRED]: { count: 1, size: 100 },
      [NegotiationStatusGroup.INTENDED]: { count: 0, size: 0 },
      [NegotiationStatusGroup.FAILED]: { count: 0, size: 0 },
    })
  })
})

describe("Implementation Status", () => {
  test("Existing implementation stati are counted", () => {
    const deals = [
      {
        current_implementation_status: "IN_OPERATION",
        deal_size: 500,
      },
      {
        current_implementation_status: "PROJECT_ABANDONED",
        deal_size: 100,
      },
      {
        current_implementation_status: undefined,
        deal_size: 1_000_000_000_000_000_000,
      },
    ] satisfies Partial<DealVersion2>[] as DealVersion2[]

    const bucketMap = deals.reduce(
      implementationStatusReducer,
      createEmptyBuckets([
        "PROJECT_NOT_STARTED",
        "STARTUP_PHASE",
        "IN_OPERATION",
        "PROJECT_ABANDONED",
      ] satisfies ImplementationStatus[] as ImplementationStatus[]),
    )

    expect(bucketMap).toEqual({
      PROJECT_NOT_STARTED: { count: 0, size: 0 },
      STARTUP_PHASE: { count: 0, size: 0 },
      IN_OPERATION: { count: 1, size: 500 },
      PROJECT_ABANDONED: { count: 1, size: 100 },
    })
  })
})
