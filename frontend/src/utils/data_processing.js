import {negotiation_status_choices} from "../choices";

export const sum = function(items, prop) {
  return items.reduce(function (a, b) {
    return a + b[prop];
  }, 0);
};

export const prepareNegotianStatusData = function(deals) {
  let stati = ['Intended', 'Concluded', 'Failed'];
  let colors = ["rgba(252,148,31,0.4)", "rgba(252,148,31,1)", "#7D4A0F"];
  let data = [];

  if (deals.length) {
    for (const [i, status] of stati.entries()) {
      let filteredDeals = deals.filter(
        d => {
          return Object.keys(negotiation_status_choices[status]).includes(d.current_negotiation_status)
        }
      );
      data.push({
        label: status,
        count: filteredDeals.length,
        size: sum(filteredDeals, 'deal_size'),
        color: colors[i],
      });
    }
  }
  return data;
}
