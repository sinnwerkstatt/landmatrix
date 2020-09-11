import Cookies from "js-cookie";

export default {
  state: () => ({
    filters: [],
    default_filters: [
      // Negotiation Status "Concluded"
      {
        field: "current_negotiation_status",
        operation: "IN",
        value: ["ORAL_AGREEMENT", "CONTRACT_SIGNED"],
      },
      // Deal size greater or equal 200ha
      // OR?! { field: "intended_size", operation: "GE", value: "200" },
      // NOTE: this might not work like before because we leave out the "intended_size"
      { field: "deal_size", operation: "GE", value: "200" },

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
      // Year unknown or >=2000
      {
        field: "initiation_year",
        operation: "GE",
        value: "2000",
        allow_null: true,
      },
    ],
  }),
  mutations: {
    setFilters(state, filters) {
      state.filters = filters;
    },
    resetFilters(state) {
      state.filters = state.default_filters;
    },
  },
  actions: {
    setFilters(context, filters) {
      Cookies.set("filters", filters, { sameSite: "lax" });
      context.commit("setFilters", filters);
    },
    resetFilters(context) {
      context.commit("resetFilters");
    },
  },
  getters: {},
};
