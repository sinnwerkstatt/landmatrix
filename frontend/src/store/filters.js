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
      // {
      //   field: "current_intention_of_investment",
      //   operation: "IN",
      //   value: [
      //     "BIOFUELS",
      //     "FOOD_CROPS",
      //     "FODDER",
      //     "LIVESTOCK",
      //     "NON_FOOD_AGRICULTURE",
      //     "AGRICULTURE_UNSPECIFIED",
      //     "TIMBER_PLANTATION",
      //     "FOREST_LOGGING", // Exclude this for Forest concession
      //     "CARBON",
      //     "FORESTRY_UNSPECIFIED",
      //     "TOURISM",
      //     "INDUSTRY",
      //     "CONVERSATION",
      //     "LAND_SPECULATION",
      //     "RENEWABLE_ENERGY",
      //     "OTHER",
      //   ],
      // },

      // Exclude Pure Contract Farming
      {
        field: "nature_of_deal",
        operation: "OVERLAP",
        value: ["OUTRIGHT_PURCHASE", "LEASE", "EXPLOITATION_PERMIT"],
      },
      // TODO: Was ist hier mit Deals die keinen nature_of_deal haben? Fliegen raus.
      // Transnational
      {
        field: "transnational",
        value: "True",
      },
      // Year unknown or >2000
      // TODO: what about unknown?
      {
        field: "initiation_date",
        operation: "GE",
        value: "2000-01-01",
      }
    ],
  }),
  mutations: {
    setFilters(state, filters) {
      state.filters = filters;
    },
    resetFilters(state) {
      state.filters = state.default_filters;
    }
  },
  actions: {
    setFilters(context, filters) {
      context.commit("setFilters", filters);
    },
    resetFilters(context) {
      context.commit("resetFilters");
    }
  },
  getters: {},
};
