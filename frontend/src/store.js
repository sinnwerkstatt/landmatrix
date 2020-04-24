import Vue from "vue";
import Vuex from "vuex";
import router from "./router";
import axios from "axios";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    user: null,
    countries: null,
    regions: null,
    wagtailRootPage: null,
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
    setUser(state, user) {
      state.user = user;
    },
    setCountries(state, countries) {
      state.countries = countries;
    },
    setRegions(state, regions) {
      state.regions = regions;
    },
    setWagtailRootPage(state, wagtailRootPage) {
      state.wagtailRootPage = wagtailRootPage;
    },
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
    fetchUser(context) {
      let query = `{ me
      { full_name username is_authenticated is_impersonate }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        context.commit("setUser", response.data.data.me);
      });
    },
    fetchCountriesAndRegions(context) {
      let query = `{ countries { id name slug } regions { id name slug } }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        context.commit("setCountries", response.data.data.countries);
        context.commit("setRegions", response.data.data.regions);
      });
    },
    fetchWagtailRootPage(context) {
      let url = `/wagtailapi/v2/pages/find/?html_path=/`;
      axios.get(url).then((response) => {
        context.commit("setWagtailRootPage", {
          map_introduction: response.data.map_introduction,
          data_introduction: response.data.data_introduction,
          footer_columns: [
            response.data.footer_column_1,
            response.data.footer_column_2,
            response.data.footer_column_3,
            response.data.footer_column_4,
          ],
        });
      });
    },
    login(context, { username, password }) {
      let query = `mutation {
        login(username: "${username}", password: "${password}") {
          status
          error
          user { full_name username is_authenticated is_impersonate }
        }
      }`;

      return new Promise(function (resolve, reject) {
        axios.post("/graphql/", { query: query }).then((response) => {
          let login_data = response.data.data.login;
          if (login_data.status === true) {
            context.commit("setUser", login_data.user);
            resolve(login_data);
          } else {
            reject(login_data);
          }
        });
      });
    },
    logout(context) {
      let query = "mutation { logout }";
      return axios.post("/graphql/", { query: query }).then((response) => {
        if (response.data.data.logout === true) {
          context.commit("setUser", null);
        }
      });
    },
    fetchWagtailPage(context, path) {
      let url = `/wagtailapi/v2/pages/find/?html_path=${path}`;
      axios.get(url).then(
        (response) => {
          let breadcrumbs;
          let title;
          if (response.data.meta.type === "wagtailcms.WagtailRootPage") {
            title = null;
            breadcrumbs = [];
          } else {
            title = response.data.title;
            breadcrumbs = [
              { link: { name: "wagtail" }, name: "Home" },
              { name: title },
            ];
          }
          context.commit("setTitle", title);
          context.commit("setBreadcrumbs", breadcrumbs);
          context.commit("setSearchDescription", response.data.meta.search_description);
          context.commit("setWagtailPage", response.data);
        },
        () => {
          router.replace({ name: "404" });
        }
      );
    },
    fetchDeals(context, options) {
      let query = `{
        deals {
          id
          target_country { id name }
          top_investors { id name }
          intention_of_investment
          negotiation_status
          implementation_status
          deal_size
        }
      }`;
      // intention_of_investment { date value }
      // negotiation_status { date value }
      // implementation_status { date value }
      axios.post("/graphql/", { query: query }).then((response) => {
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
      axios.post("/graphql/", { query: query }).then((response) => {
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
