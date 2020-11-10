import Vue from "vue";
import Vuex from "vuex";
import { pageModule } from "./page";
import filtersModule from "./filters";
import { investorModule } from "./investor";
import { mapModule } from "./map";
import axios from "axios";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    page: pageModule,
    filters: filtersModule,
    investor: investorModule,
    map: mapModule,
  },
  state: {
    formfields: {},
    chartSelectedCountry: null,
  },
  mutations: {
    setFields(state, fields) {
      state.formfields = fields;
    },
    selectChartSelectedCountry(state, country) {
      state.chartSelectedCountry = country;
    }
  },
  actions: {
    fetchBasicInfo(context) {
      let query = `{
        countries { id name slug point_lat point_lon point_lat_min point_lon_min point_lat_max point_lon_max country_page_id short_description deals {id} }
        regions { id name slug point_lat_min point_lon_min point_lat_max point_lon_max region_page_id short_description }
        me {
          full_name
          username
          is_authenticated
          is_impersonate
          userregionalinfo { country { id name } region { id name } }
          groups { id name }
        }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        context.commit("setCountries", response.data.data.countries);
        context.commit("setRegions", response.data.data.regions);
        context.commit("setUser", response.data.data.me);
      });
    },
    fetchFields(context, language = "en") {
      let query = `{ formfields(language:"${language}"){deal location contract datasource investor involvement} }`;
      axios.post("/graphql/", { query }).then((response) => {
        context.commit("setFields", response.data.data.formfields);
      });
    },
    fetchMessages(context) {
      let url = `/newdeal_legacy/messages/`;
      axios.get(url).then((response) => {
        context.commit("setMessages", response.data.messages);
      });
    },
    selectChartSelectedCountry(context, country) {
      context.commit("selectChartSelectedCountry", country)
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
  },
});

export default store;
