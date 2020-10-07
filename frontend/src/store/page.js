import axios from "axios";

export const pageModule = {
  state: () => ({
    user: null,
    countries: [],
    regions: [],
    wagtailRootPage: null,
    messages: [],
    wagtailPage: null,
    title: null,
    searchDescription: null,
    breadcrumbs: [],
    breadNav: [
      // { route: "map", icon: "fa fa-map-marker", name: "Map" },
      // { route: "deal_list", icon: "fa fa-table", name: "Data" },
      // { route: "charts", icon: "far fa-chart-bar", name: "Charts" },
      { route: "/newdeal/map/", icon: "fa fa-map-marker", name: "Map" },
      { route: "/newdeal/data/", icon: "fa fa-table", name: "Data" },
      { route: "/newdeal/charts/", icon: "far fa-chart-bar", name: "Charts" },
    ],
    showBreadcrumbs: true,
  }),
  getters: {
    countriesWithPage: (state) => {
      return state.countries.filter((c) => c.country_page_id !== null);
    },
    regionsWithPage: (state) => {
      return state.regions.filter((r) => r.region_page_id !== null);
    },
    getCountryOrRegion: (state) => ({ type, id }) => {
      return type === "region"
        ? state.regions.find((region) => region.id === +id)
        : state.countries.find((countries) => countries.id === +id);
    },
    getRegionById: (state) => (id) => {
      return state.regions.find((region) => region.id === +id);
    },
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
    setMessages(state, messages) {
      state.messages = messages;
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
    breadcrumbBar(state, visible) {
      state.showBreadcrumbs = visible;
    },
  },
  actions: {
    fetchWagtailRootPage(context) {
      let url = `/newdeal_legacy/rootpage/`;
      axios.get(url).then((response) => {
        context.commit("setWagtailRootPage", response.data);
      });
    },
    fetchWagtailPage(context, path) {
      let url = `/wagtailapi/v2/pages/find/?html_path=${path}`;
      return new Promise(function (resolve, reject) {
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
            context.commit(
              "setSearchDescription",
              response.data.meta.search_description
            );
            context.commit("setWagtailPage", response.data);
            resolve();
          },
          () => {
            reject();
          }
        );
      });
    },
    setPageContext(context, page_context) {
      context.commit("setTitle", page_context.title);
      context.commit("setBreadcrumbs", page_context.breadcrumbs);
    },
    breadcrumbBar(context, visible) {
      context.commit("breadcrumbBar", visible);
    },
  },
};
