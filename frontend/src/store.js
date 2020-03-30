import Vue from "vue";
import Vuex from "vuex";
import router from "./router";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    wagtailPage: null,
    deals: null,
    current_deal: null,
    title: null,
    searchDescription: null,
    breadcrumbs: [],
    breadNav: [
      { route: "map", icon: "fa fa-map-marker", name: "Map" },
      { route: "deal_list", icon: "fa fa-table", name: "Data" },
      { route: "charts", icon: "fa fa-bar-chart", name: "Charts" },
    ],
  },
  mutations: {
    setWagtailPage(state, wagtailPage) {
      state.wagtailPage = wagtailPage;
    },
    setDeals(state, deals) {
      state.deals = deals;
    },
    setCurrentDeal(state, deal) {
      state.current_deal = deal;
    },
    setTitle(state, title) {
      state.title = title;
    },
    setSearchDescription(state, description) {
      state.searchDescription = description;
    },
    setBreadcrumbs(state, breadcrumbs) {
      state.breadcrumbs = breadcrumbs;
    },
  },
  actions: {
    fetchWagtailPage(context, path) {
      let url = `/wagtailapi/v2/pages/find/?html_path=${path}`;
      this._vm.$http.get(url).then(
        (response) => {
          // if (response.body.meta.type === "wagtailcms.WagtailRootPage") {
          //   context.commit("setTitle", null);
          // }
          let title = response.body.title;
          context.commit("setTitle", title);
          let breads = [{ link: { name: "wagtail" }, name: "Home" }, { name: title }];
          context.commit("setBreadcrumbs", breads);
          context.commit("setSearchDescription", response.body.meta.search_description);
          context.commit("setWagtailPage", response.body.body);
        },
        (response) => {
          router.push({ name: "404" });
        }
      );
    },
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
      this._vm.$http.post("/graphql/", { query: query }).then((response) => {
        context.commit("setDeals", response.data.data.deals);
      });
    },
    setCurrentDeal(context, deal_id) {
      if (!deal_id) {
        context.commit("setCurrentDeal", null);
        return;
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
      this._vm.$http.post("/graphql/", { query: query }).then((response) => {
        context.commit("setCurrentDeal", response.data.data.deal);
      });
    },
    setPageContext(context, page_context) {
      context.commit("setTitle", page_context.title);
      context.commit("setBreadcrumbs", page_context.breadcrumbs);
    },
  },
  getters: {},
});

export default store;
