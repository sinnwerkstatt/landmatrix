import { apolloClient } from "$utils/apolloclient";
import axios from "axios";
import gql from "graphql-tag";
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
    formfields: {},
  },
  mutations: {
    setFields(state, fields) {
      state.formfields = fields;
    },
  },
  actions: {
    fetchBasicData(context) {
      let about_promise = context.dispatch("fetchAboutPages");
      let obs_promise = context.dispatch("fetchObservatoryPages");

      let rest_promise = new Promise(function (resolve, reject) {
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
                chart_descriptions {
                  web_of_transnational_deals
                  dynamics_overview
                  produce_info_map
                }
              }
            `,
          })
          .then(({ data }) => {
            context.commit("setUser", data.me);
            context.commit("setCountries", data.countries);
            context.commit("setRegions", data.regions);
            context.commit("setChartDescriptions", data.chart_descriptions);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
      return Promise.all([about_promise, obs_promise, rest_promise]);
    },
    fetchFields(context, language = "en") {
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
    fetchMessages(context) {
      let url = `/api/newdeal_legacy/messages/`;
      axios.get(url).then((response) => {
        context.commit("setMessages", response.data.messages);
      });
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
            let login_data = data.login;
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
      return new Promise(function (resolve, reject) {
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
