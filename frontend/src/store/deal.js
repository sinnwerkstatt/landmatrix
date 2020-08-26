import axios from "axios";

export const dealModule = {
  state: () => ({
    deals: [],
    deals_uptodate: false,
  }),
  mutations: {
    setDeals(state, deals) {
      state.deals = deals;
      state.deals_uptodate = true;
    },
    updateDeals(state, payload) {
      let { deals, finished } = payload;
      state.deals = state.deals.concat(deals);
      state.deals_uptodate = finished;
    },
  },
  actions: {
    fetchDeals(context, options) {
      let { limit, after } = options;
      if (context.state.deals_uptodate) return;

      let query = `{
        deals(limit:${limit}, after: ${after || -1}){
          id
          deal_size
          country { id name }
          # top_investors { id name }
          intention_of_investment
          current_negotiation_status
          current_implementation_status
          locations { id point level_of_accuracy }
        }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        let deals = response.data.data.deals;
        if (deals.length === limit) {
          context.commit("updateDeals", { deals, finished: false });
          let last_deal = deals.slice(-1)[0];
          context.dispatch("fetchDeals", { limit: limit, after: last_deal.id });
        } else {
          context.commit("updateDeals", { deals, finished: true });
        }
      });
    },
  },
  getters: {},
};
