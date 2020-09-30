import Cookies from "js-cookie";

const defaultFilters = {
  // Filters
  // Negotiation Status "Concluded"
  // Deal size greater or equal 200ha
  // OR?! { field: "intended_size", operation: "GE", value: "200" },
  // NOTE: this might not work like before because we leave out the "intended_size"
  // Initiation Year unknown or >=2000

  region_id: null,
  country_id: null,
  deal_size_min: 200,
  deal_size_max: null,
  negotiation_status: ["CONCLUDED"],
  investor: null,
  initiation_year_min: 2000,
  initiation_year_max: null,
  initiation_year_unknown: true,
  implementation_status: [],
  intention_of_investment: [],
  produce: [],
  transnational: "True",
};

const emptyFilters = {
  region_id: null,
  country_id: null,
  deal_size_min: null,
  deal_size_max: null,
  negotiation_status: [],
  investor: null,
  initiation_year_min: null,
  initiation_year_max: null,
  initiation_year_unknown: true,
  implementation_status: [],
  intention_of_investment: [],
  produce: [],
  transnational: null,
};

export default {
  state: () => ({
    filters: (() => {
      // see if we have filters in a cookie, otherwise default Filters.
      return JSON.parse(Cookies.get("filters") || JSON.stringify(defaultFilters));
    })(),
    default_filters: [
      // Exclude: Oil / Gas extraction & Mining
      {
        field: "current_intention_of_investment",
        operation: "OVERLAP",
        value: ["OIL_GAS_EXTRACTION", "MINING"],
        exclusion: true,
      },
      // Exclude Pure Contract Farming
      {
        field: "nature_of_deal",
        operation: "CONTAINED_BY",
        value: ["PURE_CONTRACT_FARMING"],
        exclusion: true,
      },
      // Transnational
      {
        field: "transnational",
        value: "True",
      },
    ],
  }),
  mutations: {
    setFilter(state, { filter, value }) {
      state.filters[filter] = value;
    },
    resetFilters(state) {
      state.filters = JSON.parse(JSON.stringify(defaultFilters));
    },
    clearFilters(state) {
      state.filters = emptyFilters;
    },
  },
  actions: {
    setFilter(context, filter) {
      context.commit("setFilter", filter);
      context.dispatch("setCookie");
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
      // if (state.filters.implementation_status.length > 0) {
      //   filters.push({
      //     field: "current_implementation_status",
      //     operation: "IN",
      //     value: state.filters.implementation_status,
      //   });
      // }
      //
      if (state.filters.investor) {
        filters.push({
          field: "operating_company",
          value: state.filters.investor.id.toString(),
        });
      }
      // if (!!state.filters.initiation_year_min) {
      //   filters.push({
      //     field: "initiation_year",
      //     operation: "GE",
      //     value: state.filters.initiation_year_min.toString(),
      //     allow_null: state.filters.initiation_year_unknown,
      //   });
      // }
      // if (!!state.filters.initiation_year_max) {
      //   filters.push({
      //     field: "initiation_year",
      //     operation: "LE",
      //     value: state.filters.initiation_year_max.toString(),
      //     allow_null: state.filters.initiation_year_unknown,
      //   });
      // }
      // if (state.filters.intention_of_investment.length > 0) {
      //   // exclude logic
      //   // TODO: use the INTENTION_CHOICES from deal.py here too?
      //   let invlist = [
      //     "BIOFUELS",
      //     "FOOD_CROPS",
      //     "FODDER",
      //     "LIVESTOCK",
      //     "NON_FOOD_AGRICULTURE",
      //     "AGRICULTURE_UNSPECIFIED",
      //     "TIMBER_PLANTATION",
      //     "FOREST_LOGGING",
      //     "CARBON",
      //     "FORESTRY_UNSPECIFIED",
      //     "MINING",
      //     "OIL_GAS_EXTRACTION",
      //     "TOURISM",
      //     "INDUSTRY",
      //     "CONVERSATION",
      //     "LAND_SPECULATION",
      //     "RENEWABLE_ENERGY",
      //     "OTHER",
      //   ];
      //   let flatflist = state.filters.intention_of_investment.map((x) => x.id);
      //   let xlist = invlist.filter((i) => {
      //     return !flatflist.includes(i);
      //   });
      //
      //   filters.push({
      //     field: "current_intention_of_investment",
      //     operation: "OVERLAP",
      //     value: xlist,
      //     exclusion: true,
      //   });
      // }
      //
      // // if (state.filters.produce && state.filters.produce.length > 0) {
      // //   let crops = [];
      // //   let animals = [];
      // //   let minerals = [];
      // //   state.filters.produce.map(prod => {
      // //     if(prod.startsWith('crop_')) crops.push(prod.replace('crop_',''));
      // //   });
      // //   if(crops.length>0) {
      // //     filters.push({
      // //     field: "current_implementation_status",
      // //     operation: "IN",
      // //     value: state.filters.implementation_status,
      // //   })
      // //   }
      // //   console.log(state.filters.produce);
      // // }
      if (state.filters.transnational) {
        filters.push({
          field: "transnational",
          value: state.filters.transnational,
        });
      }
      return filters;
    },
    currentRegionId: (state) => {
      return state.filters.region_id;
    },
    currentCountryId: (state) => {
      return state.filters.country_id;
    },
  },
};
