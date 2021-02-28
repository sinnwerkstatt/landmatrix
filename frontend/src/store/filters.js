import Cookies from "js-cookie";
import { arraysAreEqual } from "../utils";

const DEFAULT_FILTERS = {
  region_id: null,
  country_id: null,
  investor_country_id: null,
  // Deal size greater or equal 200ha
  // OR?! { field: "intended_size", operation: "GE", value: "200" },
  // NOTE: this might not work like before because we leave out the "intended_size"
  deal_size_min: 200,
  deal_size_max: null,
  // Negotiation Status "Concluded"
  negotiation_status: ["CONCLUDED"],
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

const emptyFilters = {
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

const DEFAULT_FILTER_IGNORED_KEYS = ["region_id", "country_id", "investor_country_id"];

const isDefaultFilter = (filters) => {
  let defaultKeys = Object.keys(DEFAULT_FILTERS);
  for (let key of Object.keys(filters)) {
    if (DEFAULT_FILTER_IGNORED_KEYS.includes(key)) continue;
    else if (defaultKeys.includes(key)) {
      if (Array.isArray(DEFAULT_FILTERS[key])) {
        if (!arraysAreEqual(DEFAULT_FILTERS[key], filters[key])) return false;
      } else {
        if (DEFAULT_FILTERS[key] !== filters[key]) return false;
      }
    } else return false;
  }
  return true;
};

function prepareFilters(filters) {
  let filterArray = [];
  if (filters.region_id) {
    filterArray.push({
      field: "country.fk_region_id",
      value: filters.region_id.toString(),
    });
  }
  if (filters.country_id) {
    filterArray.push({
      field: "country_id",
      value: filters.country_id.toString(),
    });
  }
  if (filters.deal_size_min) {
    filterArray.push({
      field: "deal_size",
      operation: "GE",
      value: filters.deal_size_min.toString(),
    });
  }
  if (filters.deal_size_max) {
    filterArray.push({
      field: "deal_size",
      operation: "LE",
      value: filters.deal_size_max.toString(),
    });
  }
  if (filters.negotiation_status.length > 0) {
    let negstat = [];
    if (filters.negotiation_status.includes("CONCLUDED"))
      negstat.push("ORAL_AGREEMENT", "CONTRACT_SIGNED");
    if (filters.negotiation_status.includes("INTENDED"))
      negstat.push(
        "EXPRESSION_OF_INTEREST",
        "UNDER_NEGOTIATION",
        "MEMORANDUM_OF_UNDERSTANDING"
      );
    if (filters.negotiation_status.includes("FAILED"))
      negstat.push("NEGOTIATIONS_FAILED", "CONTRACT_CANCELED");
    filterArray.push({
      field: "current_negotiation_status",
      operation: "IN",
      value: negstat,
    });
  }

  if (filters.implementation_status.length > 0) {
    filterArray.push({
      field: "current_implementation_status",
      operation: "IN",
      value: filters.implementation_status,
    });
  }

  if (filters.investor) {
    filterArray.push({
      field: "parent_companies",
      value: filters.investor.id.toString(),
    });
  }
  if (filters.investor_country_id) {
    filterArray.push({
      field: "parent_companies.country_id",
      value: filters.investor_country_id.toString(),
    });
  }
  if (filters.nature_of_deal.length > 0) {
    let nature_of_deal_choices = [
      "OUTRIGHT_PURCHASE",
      "LEASE",
      "CONCESSION",
      "EXPLOITATION_PERMIT",
      "PURE_CONTRACT_FARMING",
    ];

    let diflist = nature_of_deal_choices.filter(
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

  if (filters.initiation_year_min && filters.initiation_year_min > 1970) {
    filterArray.push({
      field: "initiation_year",
      operation: "GE",
      value: filters.initiation_year_min.toString(),
      allow_null: filters.initiation_year_unknown,
    });
  }
  if (filters.initiation_year_max) {
    filterArray.push({
      field: "initiation_year",
      operation: "LE",
      value: filters.initiation_year_max.toString(),
      allow_null: filters.initiation_year_unknown,
    });
  }

  if (filters.intention_of_investment.length > 0) {
    let intention_of_investment_choices = [
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
    let diflist = intention_of_investment_choices.filter(
      (x) => !filters.intention_of_investment.includes(x)
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
  if (filters.produce && filters.produce.length > 0) {
    let crops = [];
    let animals = [];
    let minerals = [];
    for (let prod of filters.produce) {
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
  if (!(filters.transnational === null)) {
    filterArray.push({
      field: "transnational",
      value: filters.transnational ? "True" : "False",
    });
  }
  if (filters.forest_concession) {
    filterArray.push({
      field: "forest_concession",
      value: filters.forest_concession ? "True" : "False",
    });
  }

  return filterArray;
}

export default {
  state: () => ({
    filters: (() => {
      // see if we have filters in a cookie, otherwise default Filters.
      return JSON.parse(Cookies.get("filters") || JSON.stringify(DEFAULT_FILTERS));
    })(),
    default_filters: [
      {
        field: "current_intention_of_investment",
        operation: "OVERLAP",
        value: ["OIL_GAS_EXTRACTION", "MINING"],
        exclusion: true,
      },
    ],
    isDefaultFilter: Cookies.get("filters")
      ? isDefaultFilter(JSON.parse(Cookies.get("filters")))
      : true,
    publicOnly: true,
  }),
  mutations: {
    setFilter(state, { filter, value }) {
      state.filters[filter] = value;
      if (!DEFAULT_FILTER_IGNORED_KEYS.includes(filter)) {
        state.isDefaultFilter = isDefaultFilter(state.filters);
      }
    },
    resetFilters(state) {
      state.filters = {
        ...JSON.parse(JSON.stringify(DEFAULT_FILTERS)),
        region_id: state.filters.region_id,
        country_id: state.filters.country_id,
        investor_country_id: state.filters.investor_country_id,
      };
      state.isDefaultFilter = true;
    },
    clearFilters(state) {
      state.filters = {
        ...emptyFilters,
        region_id: state.filters.region_id,
        country_id: state.filters.country_id,
        investor_country_id: state.filters.investor_country_id,
      };
      state.isDefaultFilter = false;
    },
    setPublicOnly(state, value) {
      state.publicOnly = value;
    },
  },
  actions: {
    setFilter(context, filter) {
      context.commit("setFilter", filter);
      context.dispatch("setCookie");
      // context.dispatch("fetchDeals");
    },
    resetFilters(context) {
      context.commit("resetFilters");
      context.dispatch("setCookie");
    },
    clearFilters(context) {
      context.commit("clearFilters");
      context.dispatch("setCookie");
    },
    setPublicOnly(context, value) {
      context.commit("setPublicOnly", value);
    },
    setCookie(context) {
      Cookies.set("filters", context.state.filters, { sameSite: "lax" });
    },
  },
  getters: {
    filtersForGQL: (state) => {
      return prepareFilters(state.filters);
    },
    defaultFiltersForGQL: () => (extra_filters) => {
      return prepareFilters({ ...DEFAULT_FILTERS, ...extra_filters });
    },
  },
};
