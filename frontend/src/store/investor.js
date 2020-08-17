export const investorModule = {
  state: () => ({
    investors: [],
    current_investor: null,
  }),
  mutations: {
    setCurrentInvestor(state, investor) {
      state.current_investor = investor;
    },
  },
};
