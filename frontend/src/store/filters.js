import Cookies from "js-cookie";
import { arraysAreEqual } from "../utils";

const defaultFilters = {
  region_id: null,
  country_id: null,
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

const DEFAULT_FILTER_IGNORED_KEYS = ["region_id", "country_id"];

const isDefaultFilter = (filters) => {
  let defaultKeys = Object.keys(defaultFilters);
  for (let key of Object.keys(filters)) {
    if (DEFAULT_FILTER_IGNORED_KEYS.includes(key)) continue;
    else if (defaultKeys.includes(key)) {
      if (Array.isArray(defaultFilters[key])) {
        if (!arraysAreEqual(defaultFilters[key], filters[key])) return false;
      } else {
        if (defaultFilters[key] !== filters[key]) return false;
      }
    } else return false;
  }
  return true;
};

export default {
  state: () => ({
    filters: (() => {
      // see if we have filters in a cookie, otherwise default Filters.
      return JSON.parse(Cookies.get("filters") || JSON.stringify(defaultFilters));
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
  }),
  mutations: {
    setFilter(state, { filter, value }) {
      state.filters[filter] = value;
      if (!DEFAULT_FILTER_IGNORED_KEYS.includes(filter)) {
        state.isDefaultFilter = isDefaultFilter(state.filters);
      }
    },
    resetFilters(state) {
      let region_id = state.filters.region_id;
      let country_id = state.filters.country_id;
      state.filters = JSON.parse(JSON.stringify(defaultFilters));
      state.isDefaultFilter = true;
      state.filters.region_id = region_id;
      state.filters.country_id = country_id;
    },
    clearFilters(state) {
      let region_id = state.filters.region_id;
      let country_id = state.filters.country_id;
      state.filters = emptyFilters;
      state.isDefaultFilter = false;
      state.filters.region_id = region_id;
      state.filters.country_id = country_id;
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
    setCookie(context) {
      Cookies.set("filters", context.state.filters, { sameSite: "lax" });
    },
  },
  getters: {
    filtersForGQL: (state) => {
      let filters = [];
      if (state.filters.region_id) {
        filters.push({
          field: "country.fk_region_id",
          value: state.filters.region_id.toString(),
        });
      }
      if (state.filters.country_id) {
        filters.push({
          field: "country_id",
          value: state.filters.country_id.toString(),
        });
      }
      if (state.filters.deal_size_min) {
        filters.push({
          field: "deal_size",
          operation: "GE",
          value: state.filters.deal_size_min.toString(),
        });
      }
      if (state.filters.deal_size_max) {
        filters.push({
          field: "deal_size",
          operation: "LE",
          value: state.filters.deal_size_max.toString(),
        });
      }
      if (state.filters.negotiation_status.length > 0) {
        let negstat = [];
        if (state.filters.negotiation_status.includes("CONCLUDED"))
          negstat.push("ORAL_AGREEMENT", "CONTRACT_SIGNED");
        if (state.filters.negotiation_status.includes("INTENDED"))
          negstat.push(
            "EXPRESSION_OF_INTEREST",
            "UNDER_NEGOTIATION",
            "MEMORANDUM_OF_UNDERSTANDING"
          );
        if (state.filters.negotiation_status.includes("FAILED"))
          negstat.push("NEGOTIATIONS_FAILED", "CONTRACT_CANCELED");
        filters.push({
          field: "current_negotiation_status",
          operation: "IN",
          value: negstat,
        });
      }

      if (state.filters.implementation_status.length > 0) {
        filters.push({
          field: "current_implementation_status",
          operation: "IN",
          value: state.filters.implementation_status,
        });
      }

      if (state.filters.investor) {
        filters.push({
          field: "operating_company",
          value: state.filters.investor.id.toString(),
        });
      }

      if (state.filters.nature_of_deal.length > 0) {
        let nature_of_deal_choices = [
          "OUTRIGHT_PURCHASE",
          "LEASE",
          "CONCESSION",
          "EXPLOITATION_PERMIT",
          "PURE_CONTRACT_FARMING",
        ];

        let diflist = nature_of_deal_choices.filter(
          (x) => !state.filters.nature_of_deal.includes(x)
        );
        if (diflist.length > 0) {
          filters.push({
            field: "nature_of_deal",
            operation: "CONTAINED_BY",
            value: diflist,
            exclusion: true,
          });
        }
      }

      if (
        state.filters.initiation_year_min &&
        state.filters.initiation_year_min > 1970
      ) {
        filters.push({
          field: "initiation_year",
          operation: "GE",
          value: state.filters.initiation_year_min.toString(),
          allow_null: state.filters.initiation_year_unknown,
        });
      }
      if (state.filters.initiation_year_max) {
        filters.push({
          field: "initiation_year",
          operation: "LE",
          value: state.filters.initiation_year_max.toString(),
          allow_null: state.filters.initiation_year_unknown,
        });
      }

      if (state.filters.intention_of_investment.length > 0) {
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
          (x) => !state.filters.intention_of_investment.includes(x)
        );
        if (diflist.length > 0) {
          filters.push({
            field: "current_intention_of_investment",
            operation: "OVERLAP",
            value: diflist,
            exclusion: true,
          });
        }
      }
      if (state.filters.produce && state.filters.produce.length > 0) {
        let crops = [];
        let animals = [];
        let minerals = [];
        for (let prod of state.filters.produce) {
          if (prod.id.startsWith("crop_")) crops.push(prod.value);
          if (prod.id.startsWith("animal_")) animals.push(prod.value);
          if (prod.id.startsWith("mineral_")) minerals.push(prod.value);
        }
        if (crops.length > 0) {
          filters.push({
            field: "current_crops",
            operation: "CONTAINS",
            value: crops,
          });
        }
        if (animals.length > 0) {
          filters.push({
            field: "current_animals",
            operation: "CONTAINS",
            value: animals,
          });
        }
        if (minerals.length > 0) {
          filters.push({
            field: "current_resources",
            operation: "CONTAINS",
            value: minerals,
          });
        }
      }
      if (!(state.filters.transnational === null)) {
        filters.push({
          field: "transnational",
          value: state.filters.transnational ? "True" : "False",
        });
      }
      if (state.filters.forest_concession) {
        filters.push({
          field: "forest_concession",
          value: state.filters.forest_concession ? "True" : "False",
        });
      }

      return filters;
    },
  },
};
