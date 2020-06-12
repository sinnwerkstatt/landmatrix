import Vue from "vue";
import Vuex from "vuex";
import { pageModule } from "@/store/page";
import { dealModule } from "@/store/deal";
import { investorModule } from "@/store/investor";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    page: pageModule,
    deal: dealModule,
    investor: investorModule,
  },
});

export default store;
