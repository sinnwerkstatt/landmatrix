import axios from "axios";

export const investorModule = {
  state: () => ({
    investors: [],
    current_investor: null,
    investor_fields: null,
  }),
  mutations: {
    setCurrentInvestor(state, investor) {
      state.current_investor = investor;
    },
    setInvestorFields(state, fields) {
      state.investor_fields = fields;
    },
  },
  actions: {
    setCurrentInvestor(context, investor_id) {
      if (!investor_id) {
        context.commit("setCurrentInvestor", {});
        return;
      }

      let query = `{
        investor(id:${investor_id}) {
          id
          name
          country { id name }
          classification
          homepage
          opencorporates
          comment
          # involvements
          status
          created_at
          modified_at
          deals { id country {name} }
          involvements(depth:3)
        }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        let investor = response.data.data.investor;
        context.commit("setCurrentInvestor", investor);

        let title = `${investor.name} <small>(#${investor.id})</small>`;
        context.commit("setTitle", title);
        context.commit("setBreadcrumbs", [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "investor_list" }, name: "Data" },
          { name: `Investor #${investor.id}` },
        ]);
      });
    },
  },
  getters: {},
};
