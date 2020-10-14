export const sum = function(items, prop) {
  return items.reduce(function (a, b) {
    return a + b[prop];
  }, 0);
};

export const prepareNegotianStatusData = function(deals) {
  if (deals.length) {
    let filteredDeals = {
      intended: deals.filter(
        d => {
          return ['EXPRESSION_OF_INTEREST', 'UNDER_NEGOTIATION', 'MEMORANDUM_OF_UNDERSTANDING'].includes(d.current_negotiation_status)
        }
      ),
      concluded: deals.filter(
        d => {
          return ['ORAL_AGREEMENT', 'CONTRACT_SIGNED'].includes(d.current_negotiation_status)
        }
      ),
      failed: deals.filter(
        d => {
          return ['NEGOTIATIONS_FAILED', 'CONTRACT_CANCELED'].includes(d.current_negotiation_status)
        }
      )
    }
    return [
      {
        label: "Intended",
        count: filteredDeals.intended.length,
        size: sum(filteredDeals.intended, 'deal_size'),
        color: "rgba(252,148,31,0.4)",
      },
      {
        label: "Concluded",
        count: filteredDeals.concluded.length,
        size: sum(filteredDeals.concluded, 'deal_size'),
        color: "rgba(252,148,31,1)",
      },
      {
        label: "Failed",
        count: filteredDeals.failed.length,
        size: sum(filteredDeals.failed, 'deal_size'),
        color: "#7D4A0F",
      },
    ];
  } else {
    return [];
  }
}
