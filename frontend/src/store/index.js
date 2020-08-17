import Vue from "vue";
import Vuex from "vuex";
import { pageModule } from "./page";
import { dealModule } from "./deal";
import { investorModule } from "./investor";
import axios from "axios";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    page: pageModule,
    deal: dealModule,
    investor: investorModule,
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
    fetchBasicInfo(context) {
      let query = `{
        countries { id name slug }
        regions { id name slug }
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
