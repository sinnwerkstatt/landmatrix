import Vue from "vue";
import Vuex from "vuex";
import { pageModule } from "./page";
import filtersModule from "./filters";
import { mapModule } from "./map";
import { dataModule } from "./data";
import axios from "axios";
import { apolloClient } from "/apolloclient";
import gql from "graphql-tag";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    page: pageModule,
    filters: filtersModule,
    data: dataModule,
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
                countries {
                  id
                  name
                  slug
                  point_lat
                  point_lon
                  point_lat_min
                  point_lon_min
                  point_lat_max
                  point_lon_max
                  observatory_page_id

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
                chart_descriptions
              }
            `,
          })
          .then((data) => {
            context.commit("setUser", data.data.me);
            context.commit("setCountries", data.data.countries);
            context.commit("setRegions", data.data.regions);
            context.commit("setChartDescriptions", data.data.chart_descriptions);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
      return Promise.all([obs_promise, rest_promise]);
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
        axios
          .post("/graphql/", {
            query: `
              mutation Login($username: String!, $password: String!) {
                login(username: $username, password: $password) {
                  status
                  error
                  user {
                    full_name
                    username
                    is_authenticated
                    is_impersonate
                  }
                }
              }
            `,
            variables: { username, password },
          })
          .then((response) => {
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
  },
});

export default store;
