import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    deals: null,
    current_deal: null,
    current_deal_id: null,
    title: "All Deals",
  },
  mutations: {
    setDeals(state, deals) {
      state.deals = deals;
    },
    setCurrentDeal(state, deal) {
      state.current_deal = deal;
      state.current_deal_id = deal.id;
    },
    setTitle(state, title) {
      state.title = title;
    }
  },
  actions: {
    fetchDeals(context, options) {
      let query = `{
        deals {
          id
          target_country { id name }
          top_investors { id name }
          intention_of_investment { date value }
          negotiation_status { date value }
          implementation_status { date value }
          deal_size
        }
      }`;
      this._vm.$http.post("/graphql/", {query:query})
        .then(response => {
          context.commit('setDeals', response.data.data.deals);
        });
    },
    setCurrentDeal(context, deal_id) {
      let query = `{
        deal(id:${deal_id}) {
          id
          target_country { id name }
          top_investors { id name }
          intention_of_investment { date value }
          negotiation_status { date value }
          implementation_status { date value }
          deal_size
          geojson
        }
      }`;
      this._vm.$http.post("/graphql/", {query:query})
        .then(response => {
          context.commit('setCurrentDeal', response.data.data.deal);
        });
    },
    setTitle(context, title) {
      context.commit('setTitle', title);
    }
  },
  getters: {}
});

export default store;
