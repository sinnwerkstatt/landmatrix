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
  actions: {
    fetchFields(context, language="en") {
      let query = `{ formfields(language:"${language}"){deal location contract datasource} }`;
      axios.post("/graphql/", { query }).then((response) => {
        let fields = response.data.data.formfields;
        fields.deal.location = fields.location.general_info;
        fields.deal.contract = fields.contract.general_info;
        fields.deal.datasource = fields.datasource.general_info;
        context.commit("setDealFields", fields.deal);
        // context.commit("setInvestorFields", fields.investor);
      });
    },
  },
});

export default store;
