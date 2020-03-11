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
      this._vm.$http.get(`/newdeal/api/deals/`)
        .then(response => {
          context.commit('setDeals', response.data.deals);
        });
    },
    setCurrentDeal(context, deal_id) {
      this._vm.$http.get(`/newdeal/api/deal/${deal_id}`)
        .then(response => {
          context.commit('setCurrentDeal', response.data);
        });
    },
    setTitle(context, title) {
      context.commit('setTitle', title);
    }
  },
  getters: {}
});

export default store;
