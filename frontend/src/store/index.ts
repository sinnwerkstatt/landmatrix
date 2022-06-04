import type { User } from "$types/user";
import type {
  Country,
  CountryOrRegion,
  ObservatoryPage,
  Region,
  WagtailPage,
} from "$types/wagtail";
import { apolloClient } from "$utils/apolloclient";
import {
  DEFAULT_FILTER_IGNORED_KEYS,
  DEFAULT_FILTERS,
  emptyFilters,
  isDefaultFilter,
  prepareFilters,
} from "./filters";
import type { FilterValues } from "./filters";
import { contextLayers, mapLayers } from "./map";
import type { BaseLayer, ContextLayer } from "./map";
import gql from "graphql-tag";
import Cookies from "js-cookie";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

interface PageState {
  locale: string;
  formfields: { [key: string]: any };
  // page
  user: User;
  countries: Country[];
  regions: Region[];
  aboutPages: WagtailPage[];
  observatories: ObservatoryPage[];
  messages: Array<unknown>;
  wagtailPage: WagtailPage;
  title: string;
  searchDescription: string;
  breadcrumbs: [];
  showBreadcrumbs: boolean;
  chartDescriptions: string;
  // filters
  filters: FilterValues;
  isDefaultFilter: boolean;
  publicOnly: boolean;
  signalNegstat: number;
  // map
  showFilterBar: boolean;
  showContextBar: boolean;
  displayDealsCount: boolean;
  visibleLayer: string;
  layers: BaseLayer[];
  contextLayers: ContextLayer[];
}
function isMobile() {
  return window.innerWidth < 768;
}

// see if we have filters in localStorage, otherwise default Filters.
const lSfilters = JSON.parse(
  localStorage.getItem("filters") || JSON.stringify(DEFAULT_FILTERS)
);

const store = new Vuex.Store({
  state: {
    locale: "en",
    formfields: {},
    user: null as unknown as User,
    countries: [],
    regions: [],
    aboutPages: [],
    observatories: [],
    messages: [],
    wagtailPage: null as unknown as WagtailPage,
    title: "",
    searchDescription: "",
    breadcrumbs: [],
    showBreadcrumbs: true,
    chartDescriptions: "",
    //filters
    filters: lSfilters,
    isDefaultFilter: isDefaultFilter(lSfilters),
    signalNegstat: 0,
    publicOnly: true,
    // map stuff
    showFilterBar: !isMobile(),
    showContextBar: !isMobile(),
    displayDealsCount: true,
    visibleLayer: "Map",
    layers: mapLayers,
    contextLayers: contextLayers,
  },
  getters: {
    getCountryOrRegion:
      (state: PageState) =>
      ({ type, id }: { type: string; id: number | string }): CountryOrRegion => {
        const roc =
          type === "region"
            ? state.regions.find((region) => region.id === +id)
            : state.countries.find((countries) => countries.id === +id);
        return roc ? roc : { name: "UNKNOWN" };
      },
    userAuthenticated: (state: PageState): boolean => {
      return state.user && state.user.is_authenticated;
    },
    userInGroup: (state: PageState) => (groups: string[]) => {
      if (!state.user) return false;
      return !!state.user.groups?.find((g) => groups.includes(g.name));
    },
    filtersForGQL: (state) => {
      return prepareFilters(state.filters);
    },

    defaultFiltersForGQL: () => (extra_filters: FilterValues) => {
      return prepareFilters({ ...DEFAULT_FILTERS, ...extra_filters });
    },
  },
  mutations: {
    setFields: (state, fields) => (state.formfields = fields),
    setLocale: (state, locale) => (state.locale = locale),
    setUser(state: PageState, user: User) {
      let role = "No Role";
      if (user && user.groups && user.groups.length) {
        const groupi = user.groups
          .map((g) => g.name)
          .filter((name) => {
            return (
              ["Administrators", "Editors", "Reporters", "Admin"].indexOf(name) > -1
            );
          });

        if (groupi.length) {
          let ret = "";
          if (groupi.includes("Reporters")) ret = "Reporter";
          if (groupi.includes("Editors")) ret = "Editor";
          if (groupi.includes("Administrators")) ret = "Administrator";
          const uri = user.userregionalinfo;
          if (uri) {
            let area = uri.region.map((c) => c.name);
            area = area.concat(uri.country.map((c) => c.name));
            if (area.length) {
              ret = `${ret} of ${area.join(", ")}`;
            }
          }
          role = ret;
        }
        user.bigrole = role;
      }
      state.user = user;
    },
    setCountries(state: PageState, countries: Country[]) {
      state.countries = countries;
    },
    setRegions(state: PageState, regions: Region[]) {
      state.regions = regions;
    },
    setAboutPages(state: PageState, aboutPages: WagtailPage[]) {
      state.aboutPages = aboutPages;
    },
    setObservatories(state: PageState, observatories: ObservatoryPage[]) {
      state.observatories = observatories;
    },
    setChartDescriptions(state: PageState, chartDescriptions) {
      state.chartDescriptions = chartDescriptions;
    },
    setWagtailPage(state: PageState, wagtailPage: WagtailPage) {
      state.wagtailPage = wagtailPage;
    },
    setMessages(state: PageState, messages: string[]) {
      state.messages = messages;
    },
    setTitle(state: PageState, title: string) {
      state.title = title;
    },
    setSearchDescription(state: PageState, description: string) {
      state.searchDescription = description;
    },
    setBreadcrumbs(state: PageState, breadcrumbs) {
      state.breadcrumbs = breadcrumbs;
    },
    breadcrumbBar(state: PageState, visible: boolean) {
      state.showBreadcrumbs = visible;
    },
    setFilter(state, { filter, value }) {
      state.filters[filter] = value;
      if (!DEFAULT_FILTER_IGNORED_KEYS.includes(filter)) {
        state.isDefaultFilter = isDefaultFilter(state.filters);
      }
    },
    resetFilters(state) {
      state.filters = {
        ...JSON.parse(JSON.stringify(DEFAULT_FILTERS)),
        region_id: state.filters.region_id,
        country_id: state.filters.country_id,
        investor_country_id: state.filters.investor_country_id,
      };
      state.signalNegstat = Math.random();
      state.isDefaultFilter = true;
    },
    clearFilters(state) {
      state.filters = {
        ...emptyFilters,
        region_id: state.filters.region_id,
        country_id: state.filters.country_id,
        investor_country_id: state.filters.investor_country_id,
      };
      state.signalNegstat = Math.random();
      state.isDefaultFilter = false;
    },
    setPublicOnly(state, value) {
      state.publicOnly = value;
    },
    setCurrentLayer: (state, layer) => (state.visibleLayer = layer),
    showFilterBar: (state, payload) => (state.showFilterBar = payload),
    showContextBar: (state, payload) => {
      if (payload === "!isMobile") {
        state.showContextBar = !isMobile();
      } else {
        state.showContextBar = payload;
      }
    },
    setDisplayDealsCount: (state, payload) => (state.displayDealsCount = payload),
  },
  actions: {
    async setLocale(context, locale) {
      Cookies.set("django_language", locale);
      await context.commit("setLocale", locale);
      await context.dispatch("fetchFields", locale);
      await context.dispatch("fetchChartDescriptions", locale);
      await context.dispatch("fetchAboutPages", locale);
      await context.dispatch("fetchObservatoryPages", locale);
    },
    fetchChartDescriptions(context, language = "en") {
      console.log("fetchChartDescriptions", { language });
      apolloClient
        .query({
          query: gql`
            query chart_descriptions($language: String) {
              chart_descriptions(language: $language) {
                web_of_transnational_deals
                dynamics_overview
                produce_info_map
              }
            }
          `,
          variables: { language },
        })
        .then(({ data }) => {
          context.commit("setChartDescriptions", data.chart_descriptions);
        });
    },
    fetchBasicData(context) {
      return new Promise<void>(function (resolve, reject) {
        apolloClient
          .query({
            query: gql`
              {
                me {
                  id
                  full_name
                  username
                  initials
                  is_authenticated
                  is_impersonate
                  role
                  userregionalinfo {
                    country {
                      id
                      name
                    }
                    region {
                      id
                      name
                    }
                  }
                  groups {
                    id
                    name
                  }
                }
                countries {
                  id
                  name
                  code_alpha2
                  slug
                  point_lat
                  point_lon
                  point_lat_min
                  point_lon_min
                  point_lat_max
                  point_lon_max
                  observatory_page_id
                  high_income
                  deals {
                    id
                  }
                }
                regions {
                  id
                  name
                  slug
                  point_lat_min
                  point_lon_min
                  point_lat_max
                  point_lon_max
                  observatory_page_id
                }
              }
            `,
          })
          .then(({ data }) => {
            context.commit("setUser", data.me);
            context.commit("setCountries", data.countries);
            context.commit("setRegions", data.regions);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    fetchFields(context, language = "en") {
      console.debug("fetchFields", { language });
      apolloClient
        .query({
          query: gql`
            query FormFields($language: String) {
              formfields(language: $language) {
                deal
                location
                contract
                datasource
                investor
                involvement
              }
            }
          `,
          variables: { language },
        })
        .then((data) => {
          context.commit("setFields", data.data.formfields);
        });
    },
    async fetchMessages(context) {
      const res = await (await fetch(`/api/newdeal_legacy/messages/`)).json();
      context.commit("setMessages", res.messages);
    },

    login(context, { username, password }) {
      return new Promise(function (resolve, reject) {
        apolloClient
          .mutate({
            mutation: gql`
              mutation Login($username: String!, $password: String!) {
                login(username: $username, password: $password) {
                  status
                  error
                  user {
                    full_name
                    username
                    is_authenticated
                    is_impersonate
                    userregionalinfo {
                      country {
                        id
                        name
                      }
                      region {
                        id
                        name
                      }
                    }
                    groups {
                      id
                      name
                    }
                  }
                }
              }
            `,
            variables: { username, password },
          })
          .then(({ data }) => {
            const login_data = data.login;
            if (login_data.status === true) {
              context.commit("setUser", login_data.user);
              resolve(login_data);
            } else {
              reject(login_data);
            }
          });
      });
    },
    logout() {
      return new Promise<void>(function (resolve, reject) {
        apolloClient
          .mutate({
            mutation: gql`
              mutation {
                logout
              }
            `,
          })
          .then(({ data }) => {
            if (data.logout === true) resolve();
            else reject();
          })
          .catch(reject);
      });
    },
    async fetchObservatoryPages(context, language = "en") {
      console.log("fetchObservatoryPages", { language });
      const url = `/wagtailapi/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
      const res = await (await fetch(url)).json();
      context.commit("setObservatories", res.items);
    },
    async fetchAboutPages(context, language = "en") {
      console.debug("fetchAboutPages", { language });
      const url = `/wagtailapi/v2/pages/?order=title&type=wagtailcms.AboutIndexPage`;
      const res = await (await fetch(url)).json();
      const indexPageId = res.items[0].id;

      const pagesUrl = `/wagtailapi/v2/pages/?child_of=${indexPageId}`;
      const res_children = await (await fetch(pagesUrl)).json();
      context.commit("setAboutPages", res_children.items);
    },
    async fetchWagtailPage(context, path) {
      const url = `/wagtailapi/v2/pages/find/?html_path=${path}`;
      const res = await (await fetch(url)).json();
      let breadcrumbs;
      let title;
      if (res.meta.type === "wagtailcms.WagtailRootPage") {
        title = null;
        breadcrumbs = [{ name: "Home" }];
      } else {
        title = res.title;
        breadcrumbs = [{ link: { name: "wagtail" }, name: "Home" }, { name: title }];
      }
      context.commit("setTitle", title);
      context.commit("setBreadcrumbs", breadcrumbs);
      context.commit("setSearchDescription", res.meta.search_description);
      context.commit("setWagtailPage", res);
    },
    setPageContext(context, page_context) {
      context.commit("setTitle", page_context.title);
      context.commit("setBreadcrumbs", page_context.breadcrumbs);
    },
    breadcrumbBar(context, visible: boolean) {
      context.commit("breadcrumbBar", visible);
    },
    setFilter(context, filter) {
      // TODO-3 temporary cleanup situation for old localStorage-sessions. should be able to remove this in mid2022
      if (filter.filter === "negotiation_status") {
        const valid_choices = [
          "EXPRESSION_OF_INTEREST",
          "UNDER_NEGOTIATION",
          "MEMORANDUM_OF_UNDERSTANDING",
          "ORAL_AGREEMENT",
          "CONTRACT_SIGNED",
          "CHANGE_OF_OWNERSHIP",
          "NEGOTIATIONS_FAILED",
          "CONTRACT_CANCELED",
          "CONTRACT_EXPIRED",
        ];
        filter.value = filter.value.filter((f: string) => valid_choices.includes(f));
      }
      context.commit("setFilter", filter);
      context.dispatch("setStorage");
      // context.dispatch("fetchDeals");
    },
    resetFilters(context) {
      context.commit("resetFilters");
      context.dispatch("setStorage");
    },
    clearFilters(context) {
      context.commit("clearFilters");
      context.dispatch("setStorage");
    },
    setPublicOnly(context, value) {
      context.commit("setPublicOnly", value);
    },
    setStorage(context) {
      localStorage.setItem("filters", JSON.stringify(context.state.filters));
    },
    setCurrentLayer: (context, layer) => context.commit("setCurrentLayer", layer),
    showFilterBar: (context, payload) => context.commit("showFilterBar", payload),
    showContextBar: (context, payload) => context.commit("showContextBar", payload),
  },
});

export default store;
