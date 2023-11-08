import { createEmptyBuckets } from "$lib/data/buckets"
import { agricultureIntentionReducer } from "$lib/data/charts/agricultureIntention"
import { implementationStatusReducer } from "$lib/data/charts/implementationStatus"
import { intentionOfInvestmentGroupReducer } from "$lib/data/charts/intentionOfInvestmentGroup"
import { negotiationStatusGroupReducer } from "$lib/data/charts/negotiationStatusGroup"
import { produceGroupReducer } from "$lib/data/charts/produceGroup"
import type { Deal } from "$lib/types/deal"
import {
  AgricultureIoI,
  ForestryIoI,
  ImplementationStatus,
  IoIGroup,
  NegotiationStatus,
  NegotiationStatusGroup,
  OtherIoI,
  ProduceGroup,
  RenewableEnergyIoI,
} from "$lib/types/deal"

describe("Intention of Investment Group", () => {
  test("Multiple intentions of same group per deal are counted as 1", () => {
    const deals = [
      {
        current_intention_of_investment: [
          ForestryIoI.CARBON,
          ForestryIoI.TIMBER_PLANTATION,
          ForestryIoI.FOREST_LOGGING,
          RenewableEnergyIoI.SOLAR_PARK,
          AgricultureIoI.BIOFUELS,
        ],
        deal_size: 500,
      },
      {
        current_intention_of_investment: [
          OtherIoI.MINING,
          OtherIoI.CONVERSATION,
          AgricultureIoI.BIOFUELS,
          RenewableEnergyIoI.WIND_FARM,
        ],
        deal_size: 100,
      },
    ] as Deal[]

    const bucketMap = deals.reduce(
      intentionOfInvestmentGroupReducer,
      createEmptyBuckets(Object.values(IoIGroup)),
    )

    expect(bucketMap).toEqual({
      [IoIGroup.FORESTRY]: { count: 1, size: 500 },
      [IoIGroup.AGRICULTURE]: { count: 2, size: 600 },
      [IoIGroup.RENEWABLE_ENERGY]: { count: 2, size: 600 },
      [IoIGroup.OTHER]: { count: 1, size: 100 },
    })
  })
})

describe("Agriculture Intention of Investment", () => {
  test("Only count agriculture intentions", () => {
    const deals = [
      {
        current_intention_of_investment: [
          ForestryIoI.CARBON,
          ForestryIoI.FOREST_LOGGING,
          AgricultureIoI.BIOFUELS,
        ],
        deal_size: 500,
      },
      {
        current_intention_of_investment: [
          OtherIoI.MINING,
          AgricultureIoI.BIOFUELS,
          AgricultureIoI.FOOD_CROPS,
        ],
        deal_size: 100,
      },
    ] as Deal[]

    const bucketMap = deals.reduce(
      agricultureIntentionReducer,
      createEmptyBuckets(Object.values(AgricultureIoI)),
    )

    expect(bucketMap).toEqual({
      [AgricultureIoI.BIOFUELS]: { count: 2, size: 600 },
      [AgricultureIoI.BIOMASS_ENERGY_GENERATION]: { count: 0, size: 0 },
      [AgricultureIoI.FOOD_CROPS]: { count: 1, size: 100 },
      [AgricultureIoI.FODDER]: { count: 0, size: 0 },
      [AgricultureIoI.LIVESTOCK]: { count: 0, size: 0 },
      [AgricultureIoI.NON_FOOD_AGRICULTURE]: { count: 0, size: 0 },
      [AgricultureIoI.AGRICULTURE_UNSPECIFIED]: { count: 0, size: 0 },
    })
  })
})

describe("Produce Group", () => {
  test("Count non empty existing fields", () => {
    const deals = [
      {
        current_animals: ["cows", "bees"],
        current_crops: ["corn"],
        deal_size: 500,
      },
      {
        current_animals: ["sloths"],
        current_mineral_resources: [],
        deal_size: 100,
      },
    ] as Deal[]

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
        current_negotiation_status: NegotiationStatus.CONTRACT_SIGNED,
        deal_size: 500,
      },
      {
        current_negotiation_status: NegotiationStatus.CONTRACT_EXPIRED,
        deal_size: 100,
      },
      {
        current_implementation_status: undefined,
        deal_size: 1_000_000_000_000_000_000,
      },
    ] as Deal[]

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
        current_implementation_status: ImplementationStatus.IN_OPERATION,
        deal_size: 500,
      },
      {
        current_implementation_status: ImplementationStatus.PROJECT_ABANDONED,
        deal_size: 100,
      },
      {
        current_implementation_status: undefined,
        deal_size: 1_000_000_000_000_000_000,
      },
    ] as Deal[]

    const bucketMap = deals.reduce(
      implementationStatusReducer,
      createEmptyBuckets(Object.values(ImplementationStatus)),
    )

    expect(bucketMap).toEqual({
      [ImplementationStatus.PROJECT_NOT_STARTED]: { count: 0, size: 0 },
      [ImplementationStatus.STARTUP_PHASE]: { count: 0, size: 0 },
      [ImplementationStatus.IN_OPERATION]: { count: 1, size: 500 },
      [ImplementationStatus.PROJECT_ABANDONED]: { count: 1, size: 100 },
    })
  })
})
