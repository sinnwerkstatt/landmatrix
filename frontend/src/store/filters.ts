import type { GQLFilter } from "$types/filters";
import type { Investor } from "$types/investor";
import { isEqual } from "lodash-es";

interface Produce {
  name: string;
  id: string;
  value: string;
}

export interface FilterValues {
  region_id: number | null;
  country_id: number | null;
  investor_country_id: number | null;
  deal_size_min: number | null;
  deal_size_max: number | null;
  negotiation_status: string[];
  nature_of_deal: string[];
  investor: null | Investor;
  initiation_year_min: number | null;
  initiation_year_max: number | null;
  initiation_year_unknown: boolean;
  implementation_status: string[];
  intention_of_investment: string[];
  produce: Produce[];
  transnational: boolean | null;
  forest_concession: boolean | null;
  [key: string]: null | string | number | boolean | string[] | Investor | Produce[];
}

export const DEFAULT_FILTERS: FilterValues = {
  region_id: null,
  country_id: null,
  investor_country_id: null,
  // Deal size greater or equal 200ha
  // OR?! { field: "intended_size", operation: "GE", value: "200" },
  // NOTE: this might not work like before because we leave out the "intended_size"
  deal_size_min: 200,
  deal_size_max: null,
  // Negotiation Status "Concluded"
  negotiation_status: ["ORAL_AGREEMENT", "CONTRACT_SIGNED", "CHANGE_OF_OWNERSHIP"],
  // Exclude Pure Contract Farming
  nature_of_deal: ["OUTRIGHT_PURCHASE", "LEASE", "CONCESSION", "EXPLOITATION_PERMIT"],
  investor: null,
  // Initiation Year unknown or >=2000
  initiation_year_min: 2000,
  initiation_year_max: null,
  initiation_year_unknown: true,
  implementation_status: [],
  // Exclude: Oil / Gas extraction & Mining
  intention_of_investment: [
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
    "TOURISM",
    "INDUSTRY",
    "CONVERSATION",
    "LAND_SPECULATION",
    "RENEWABLE_ENERGY",
    "OTHER",
  ],
  produce: [],
  // Transnational True
  transnational: true,
  forest_concession: false,
};

export const emptyFilters: FilterValues = {
  region_id: null,
  country_id: null,
  investor_country_id: null,
  deal_size_min: null,
  deal_size_max: null,
  negotiation_status: [],
  nature_of_deal: [],
  investor: null,
  initiation_year_min: null,
  initiation_year_max: null,
  initiation_year_unknown: true,
  implementation_status: [],
  intention_of_investment: [],
  produce: [],
  transnational: null,
  forest_concession: null,
};

export const DEFAULT_FILTER_IGNORED_KEYS = [
  "region_id",
  "country_id",
  "investor_country_id",
];

export const isDefaultFilter = (filters: FilterValues): boolean => {
  const defaultKeys = Object.keys(DEFAULT_FILTERS);
  for (const key of Object.keys(filters)) {
    if (DEFAULT_FILTER_IGNORED_KEYS.includes(key)) continue;
    else if (defaultKeys.includes(key)) {
      if (Array.isArray(DEFAULT_FILTERS[key])) {
        if (!isEqual(DEFAULT_FILTERS[key], filters[key])) return false;
      } else {
        if (DEFAULT_FILTERS[key] !== filters[key]) return false;
      }
    } else return false;
  }
  return true;
};

export function prepareFilters(filters: FilterValues): GQLFilter[] {
  const filterArray = [] as GQLFilter[];

  if (filters.region_id)
    filterArray.push({ field: "country.region_id", value: filters.region_id });

  if (filters.country_id)
    filterArray.push({ field: "country_id", value: filters.country_id });

  if (filters.deal_size_min)
    filterArray.push({
      field: "deal_size",
      operation: "GE",
      value: filters.deal_size_min,
    });

  if (filters.deal_size_max) {
    filterArray.push({
      field: "deal_size",
      operation: "LE",
      value: filters.deal_size_max,
    });
  }
  if (filters.negotiation_status.length > 0) {
    filterArray.push({
      field: "current_negotiation_status",
      operation: "IN",
      value: filters.negotiation_status,
    });
  }

  if (filters.implementation_status.length > 0) {
    filterArray.push({
      field: "current_implementation_status",
      operation: "IN",
      value: filters.implementation_status,
      allow_null: filters.implementation_status.includes("UNKNOWN"),
    });
  }

  if (filters.investor)
    filterArray.push({ field: "parent_companies", value: filters.investor.id });

  if (filters.investor_country_id) {
    filterArray.push({
      field: "parent_companies.country_id",
      value: filters.investor_country_id,
    });
  }
  if (filters.nature_of_deal.length > 0) {
    const nature_of_deal_choices = [
      "OUTRIGHT_PURCHASE",
      "LEASE",
      "CONCESSION",
      "EXPLOITATION_PERMIT",
      "PURE_CONTRACT_FARMING",
    ];

    const diflist = nature_of_deal_choices.filter(
      (x) => !filters.nature_of_deal.includes(x)
    );
    if (diflist.length > 0) {
      filterArray.push({
        field: "nature_of_deal",
        operation: "CONTAINED_BY",
        value: diflist,
        exclusion: true,
      });
    }
  }

  if (filters.initiation_year_min && filters.initiation_year_min > 1970)
    filterArray.push({
      field: "initiation_year",
      operation: "GE",
      value: filters.initiation_year_min,
      allow_null: filters.initiation_year_unknown,
    });

  if (filters.initiation_year_max)
    filterArray.push({
      field: "initiation_year",
      operation: "LE",
      value: filters.initiation_year_max,
      allow_null: filters.initiation_year_unknown,
    });

  if (filters.intention_of_investment.length > 0)
    filterArray.push({
      field: "current_intention_of_investment",
      operation: "OVERLAP",
      value: filters.intention_of_investment.filter((x) => x !== "UNKNOWN"),
      allow_null: filters.intention_of_investment.includes("UNKNOWN"),
    });

  if (filters.produce && filters.produce.length > 0) {
    const crops = [];
    const animals = [];
    const minerals = [];
    for (const prod of filters.produce) {
      if (prod.id.startsWith("crop_")) crops.push(prod.value);
      if (prod.id.startsWith("animal_")) animals.push(prod.value);
      if (prod.id.startsWith("mineral_")) minerals.push(prod.value);
    }
    if (crops.length > 0) {
      filterArray.push({ field: "current_crops", operation: "CONTAINS", value: crops });
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
  if (filters.transnational !== null)
    filterArray.push({ field: "transnational", value: filters.transnational });

  if (filters.forest_concession !== null)
    filterArray.push({ field: "forest_concession", value: filters.forest_concession });

  return filterArray;
}
