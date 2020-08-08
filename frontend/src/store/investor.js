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
};
