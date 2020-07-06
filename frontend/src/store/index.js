import Vue from "vue";
import Vuex from "vuex";
import { pageModule } from "@/store/page";
import { dealModule } from "@/store/deal";
import { investorModule } from "@/store/investor";
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
      let query = `{ formfields(language:"${language}"){deal} }`;
      axios.post("/graphql/", { query }).then((response) => {
        let fields = response.data.data.formfields;
        context.commit("setDealFields", fields.deal);
        // context.commit("setInvestorFields", fields.investor);
      });
    },
  },
});

export default store;
