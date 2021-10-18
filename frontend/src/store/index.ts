import { apolloClient } from "$utils/apolloclient";
import gql from "graphql-tag";
import Cookies from "js-cookie";
import Vue from "vue";
import Vuex from "vuex";
import filtersModule from "./filters";
import { mapModule } from "./map";
import { pageModule } from "./page";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    page: pageModule,
    filters: filtersModule,
    map: mapModule,
  },
  state: {
    locale: "en",
    formfields: {},
  },
  mutations: {
    setFields: (state, fields) => (state.formfields = fields),
    setLocale: (state, locale) => (state.locale = locale),
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
  },
});

export default store;
