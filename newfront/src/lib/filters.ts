import type { Investor } from "./types/investor";
import type { GQLFilter } from "./types/filters";
import { writable } from "svelte/store";

interface Produce {
  name: string;
  id: string;
  value: string;
}

enum NegotiationStatus {
  EXPRESSION_OF_INTEREST = "EXPRESSION_OF_INTEREST",
  UNDER_NEGOTIATION = "UNDER_NEGOTIATION",
  MEMORANDUM_OF_UNDERSTANDING = "MEMORANDUM_OF_UNDERSTANDING",
  ORAL_AGREEMENT = "ORAL_AGREEMENT",
  CONTRACT_SIGNED = "CONTRACT_SIGNED",
  NEGOTIATIONS_FAILED = "NEGOTIATIONS_FAILED",
  CONTRACT_CANCELED = "CONTRACT_CANCELED",
  CONTRACT_EXPIRED = "CONTRACT_EXPIRED",
  CHANGE_OF_OWNERSHIP = "CHANGE_OF_OWNERSHIP",
}
enum NatureOfDeal {
  OUTRIGHT_PURCHASE = "OUTRIGHT_PURCHASE",
  LEASE = "LEASE",
  CONCESSION = "CONCESSION",
  EXPLOITATION_PERMIT = "EXPLOITATION_PERMIT",
  PURE_CONTRACT_FARMING = "PURE_CONTRACT_FARMING",
}
enum ImplementationStatus {
  PROJECT_NOT_STARTED = "PROJECT_NOT_STARTED",
  STARTUP_PHASE = "STARTUP_PHASE",
  IN_OPERATION = "IN_OPERATION",
  PROJECT_ABANDONED = "PROJECT_ABANDONED",
}
enum IntentionOfInvestment {
  BIOFUELS = "BIOFUELS",
  FOOD_CROPS = "FOOD_CROPS",
  FODDER = "FODDER",
  LIVESTOCK = "LIVESTOCK",
  NON_FOOD_AGRICULTURE = "NON_FOOD_AGRICULTURE",
  AGRICULTURE_UNSPECIFIED = "AGRICULTURE_UNSPECIFIED",
  TIMBER_PLANTATION = "TIMBER_PLANTATION",
  FOREST_LOGGING = "FOREST_LOGGING",
  CARBON = "CARBON",
  FORESTRY_UNSPECIFIED = "FORESTRY_UNSPECIFIED",
  MINING = "MINING",
  OIL_GAS_EXTRACTION = "OIL_GAS_EXTRACTION",
  TOURISM = "TOURISM",
  INDUSTRY = "INDUSTRY",
  CONVERSATION = "CONVERSATION",
  LAND_SPECULATION = "LAND_SPECULATION",
  RENEWABLE_ENERGY = "RENEWABLE_ENERGY",
  OTHER = "OTHER",
}

export class FilterValues {
  region_id: number;
  country_id: number;
  investor_country_id: number;
  deal_size_min: number;
  deal_size_max: number;
  negotiation_status: NegotiationStatus[] = [];
  nature_of_deal: NatureOfDeal[] = [];
  investor: Investor;
  initiation_year_min: number;
  initiation_year_max: number;
  initiation_year_unknown = true;
  implementation_status: ImplementationStatus[] = [];
  intention_of_investment: IntentionOfInvestment[] = [];
  produce: Produce[] = [];
  transnational: boolean;
  forest_concession: boolean; // Forest concession False

  public default() {
    // Deal size greater or equal 200ha
    // OR?! { field: "intended_size", operation: "GE", value: "200" },
    // NOTE: this might not work like before because we leave out the "intended_size"
    this.deal_size_min = 200;
    // Negotiation Status "Concluded"
    this.negotiation_status = [
      NegotiationStatus.ORAL_AGREEMENT,
      NegotiationStatus.CONTRACT_SIGNED,
    ];
    // Exclude Pure Contract Farming
    this.nature_of_deal = [
      NatureOfDeal.OUTRIGHT_PURCHASE,
      NatureOfDeal.LEASE,
      NatureOfDeal.CONCESSION,
      NatureOfDeal.EXPLOITATION_PERMIT,
    ];
    // Initiation Year unknown or >=2000
    this.initiation_year_min = 2000;
    // Exclude: Oil / Gas extraction & Mining
    this.intention_of_investment = [
      IntentionOfInvestment.BIOFUELS,
      IntentionOfInvestment.FOOD_CROPS,
      IntentionOfInvestment.FODDER,
      IntentionOfInvestment.LIVESTOCK,
      IntentionOfInvestment.NON_FOOD_AGRICULTURE,
      IntentionOfInvestment.AGRICULTURE_UNSPECIFIED,
      IntentionOfInvestment.TIMBER_PLANTATION,
      IntentionOfInvestment.FOREST_LOGGING,
      IntentionOfInvestment.CARBON,
      IntentionOfInvestment.FORESTRY_UNSPECIFIED,
      IntentionOfInvestment.TOURISM,
      IntentionOfInvestment.INDUSTRY,
      IntentionOfInvestment.CONVERSATION,
      IntentionOfInvestment.LAND_SPECULATION,
      IntentionOfInvestment.RENEWABLE_ENERGY,
      IntentionOfInvestment.OTHER,
    ];
    // Transnational True
    this.transnational = true;
    // Forest concession False
    this.forest_concession = false;
    return this;
  }
  public toGQLFilterArray(): GQLFilter[] {
    const filterArray: GQLFilter[] = [];

    if (this.region_id)
      filterArray.push({ field: "country.fk_region_id", value: this.region_id });

    if (this.country_id)
      filterArray.push({ field: "country_id", value: this.country_id });

    if (this.deal_size_min)
      filterArray.push({
        field: "deal_size",
        operation: "GE",
        value: this.deal_size_min,
      });

    if (this.deal_size_max)
      filterArray.push({
        field: "deal_size",
        operation: "LE",
        value: this.deal_size_max,
      });

    if (this.negotiation_status.length > 0)
      filterArray.push({
        field: "current_negotiation_status",
        operation: "IN",
        value: this.negotiation_status,
      });

    if (this.implementation_status.length > 0)
      filterArray.push({
        field: "current_implementation_status",
        operation: "IN",
        value: this.implementation_status,
        allow_null: this.implementation_status.includes("UNKNOWN"),
      });

    if (this.investor)
      filterArray.push({ field: "parent_companies", value: this.investor.id });

    if (this.investor_country_id)
      filterArray.push({
        field: "parent_companies.country_id",
        value: this.investor_country_id,
      });

    if (this.nature_of_deal.length > 0) {
      //TODO use enum
      const nature_of_deal_choices = [
        "OUTRIGHT_PURCHASE",
        "LEASE",
        "CONCESSION",
        "EXPLOITATION_PERMIT",
        "PURE_CONTRACT_FARMING",
      ];

      const diflist = nature_of_deal_choices.filter(
        (x) => !this.nature_of_deal.includes(x)
      );
      if (diflist.length > 0)
        filterArray.push({
          field: "nature_of_deal",
          operation: "CONTAINED_BY",
          value: diflist,
          exclusion: true,
        });
    }

    if (this.initiation_year_min && this.initiation_year_min > 1970)
      filterArray.push({
        field: "initiation_year",
        operation: "GE",
        value: this.initiation_year_min,
        allow_null: this.initiation_year_unknown,
      });

    if (this.initiation_year_max)
      filterArray.push({
        field: "initiation_year",
        operation: "LE",
        value: this.initiation_year_max,
        allow_null: this.initiation_year_unknown,
      });

    if (this.intention_of_investment.length > 0) {
      const intention_of_investment_choices = [
        "BIOFUELS",
        "FOOD_CROPS",
        "FODDER",
        "LIVESTOCK",
        "NON_FOOD_AGRICULTURE",
        "AGRICULTURE_UNSPECIFIED",
        "TIMBER_PLANTATION",
        "FOREST_LOGGING",
        "CARBON",
        "FORESTRY_UNSPECIFIED",
        "MINING",
        "OIL_GAS_EXTRACTION",
        "TOURISM",
        "INDUSTRY",
        "CONVERSATION",
        "LAND_SPECULATION",
        "RENEWABLE_ENERGY",
        "OTHER",
      ];
      const diflist = intention_of_investment_choices.filter(
        (x) => !this.intention_of_investment.includes(x)
      );
      if (diflist.length > 0) {
        filterArray.push({
          field: "current_intention_of_investment",
          operation: "OVERLAP",
          value: diflist,
          exclusion: true,
        });
      }
    }

    if (this.produce && this.produce.length > 0) {
      const crops = [];
      const animals = [];
      const minerals = [];
      for (const prod of this.produce) {
        if (prod.id.startsWith("crop_")) crops.push(prod.value);
        if (prod.id.startsWith("animal_")) animals.push(prod.value);
        if (prod.id.startsWith("mineral_")) minerals.push(prod.value);
      }
      if (crops.length > 0) {
        filterArray.push({
          field: "current_crops",
          operation: "CONTAINS",
          value: crops,
        });
      }
      if (animals.length > 0) {
        filterArray.push({
          field: "current_animals",
          operation: "CONTAINS",
          value: animals,
        });
      }
      if (minerals.length > 0) {
        filterArray.push({
          field: "current_mineral_resources",
          operation: "CONTAINS",
          value: minerals,
        });
      }
    }

    if (this.transnational !== null)
      filterArray.push({ field: "transnational", value: this.transnational });

    if (this.forest_concession !== null)
      filterArray.push({ field: "forest_concession", value: this.forest_concession });

    return filterArray;
  }
}

export const defaultFilterValues = () => new FilterValues().default();

// export const DEFAULT_FILTER_IGNORED_KEYS = [
//   "region_id",
//   "country_id",
//   "investor_country_id",
// ];
//
// export const isDefaultFilter = (filters: FilterValues): boolean => {
//   const defaultKeys = Object.keys(DEFAULT_FILTERS);
//   for (const key of Object.keys(filters)) {
//     if (DEFAULT_FILTER_IGNORED_KEYS.includes(key)) continue;
//     else if (defaultKeys.includes(key)) {
//       if (Array.isArray(DEFAULT_FILTERS[key])) {
//         if (!isEqual(DEFAULT_FILTERS[key], filters[key])) return false;
//       } else {
//         if (DEFAULT_FILTERS[key] !== filters[key]) return false;
//       }
//     } else return false;
//   }
//   return true;
// };
//

function createFilters() {
  const { subscribe, set, update } = writable(new FilterValues());

  return {
    subscribe,
    set: ({ filter, value }) =>
      update((fltrs) => {
        fltrs[filter] = value;
        return fltrs;
      }),
    // increment: () => update((n) => n + 1),
    // decrement: () => update((n) => n - 1),
    // reset: () => set(new FilterValues()),
  };
}

export const filters = createFilters();

filters.subscribe((x) => {
  console.log("FILTER UPDATE", x);
});
