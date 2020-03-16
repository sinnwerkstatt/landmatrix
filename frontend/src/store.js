import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    deals: null,
    current_deal: null,
    title: "All Deals",
    breadcrumbs: [],
  },
  mutations: {
    setDeals(state, deals) {
      state.deals = deals;
    },
    setCurrentDeal(state, deal) {
      state.current_deal = deal;
    },
    setTitle(state, title) {
      state.title = title;
    },
    setBreadcrumbs(state, breadcrumbs) {
      state.breadcrumbs = breadcrumbs;
    },
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
      if (!deal_id) {
        context.commit('setCurrentDeal', null);
        return
      }

      let query = `{
        deal(id:${deal_id}) {
          id
          target_country { id name }
          top_investors { id name }
          intention_of_investment { date value }
          negotiation_status { date value }
          implementation_status { date value }
          deal_size
          intended_size
          contract_size { date value }
          production_size { date value }
          geojson
        }
      }`;
      this._vm.$http.post("/graphql/", {query:query})
        .then(response => {
          context.commit('setCurrentDeal', response.data.data.deal);
        });
    },
    setPageContext(context, page_context) {
      context.commit('setTitle', page_context.title);
      context.commit('setBreadcrumbs', page_context.breadcrumbs);
    },
  },
  getters: {}
});

export default store;
