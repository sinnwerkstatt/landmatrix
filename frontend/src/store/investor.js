export const investorModule = {
  state: () => ({
    investors: [],
    current_investor: null,
  }),
  getters: {
    getInvestor: (state) => (id) => {
      return state.investors.find((i) => i.id === +id);
    },
  },
  mutations: {
    setCurrentInvestor(state, investor) {
      state.current_investor = investor;
    },
    setInvestors(state, investors) {
      state.investors = investors;
    },
  },
};
