import {
  implementation_status_choices,
  intention_of_investment_map,
  negotiation_status_map,
  classification_choices,
} from "/choices";

export const getDealValue = function(component, deal, fieldName) {
  switch (fieldName) {
    case('id'): {
      let location = {name: 'deal_detail', params: {deal_id: deal.id}};
      let url = component.$router.resolve(location).href;
      return `<a class="label label-deal" href="${url}">${deal.id}</a>`;
    }
    case('deal_size'): return deal.deal_size.toLocaleString();
    case('intended_size'): return deal.intended_size? deal.intended_size.toLocaleString(): null;

    case('country'): {
      let country = component.$store.getters.getCountryOrRegion({
        type: "country",
        id: deal.country.id,
      });
      return country ? country.name : "";
    }
    case('intention_of_investment'): {
      let intentions;
      if (deal.current_intention_of_investment) {
        intentions = deal.current_intention_of_investment
          .map((ioi) => {
            let [intention, icon] = intention_of_investment_map[ioi];
            return `<span class="ioi-label"><i class="${icon}"></i> ${component.$t(
              intention
            )}</span> `;
          })
          .join(" ");
      }
      return intentions;
    }
    case('current_negotiation_status'): {
      //TODO: Why is there deals with current_negotiation_status === null?
      let [neg_status, neg_status_group] = ["UNDEFINED", null];
      if (deal.current_negotiation_status) {
        [neg_status, neg_status_group] = negotiation_status_map[
          deal.current_negotiation_status
          ];
      }
      return neg_status_group
        ? `${neg_status_group} (${neg_status})`
        : neg_status;
    }
    case('current_implementation_status'): {
      return deal.current_implementation_status
        ? implementation_status_choices[deal.current_implementation_status]
        : "None";
    }
    default: {
      return deal[fieldName];
    }
  }
}


export const getInvestorValue = function(component, investor, fieldName) {
  switch (fieldName) {
    case('id'): {
      let location = {name: 'investor_detail', params: {investor_id: investor.id}};
      let url = component.$router.resolve(location).href;
      return `<a class="label label-investor" href="${url}">${investor.id}</a>`;
    }
    case('country'): {
      let country = null;
      if (investor.country) {
        country = component.$store.getters.getCountryOrRegion({
          type: "country",
          id: investor.country.id,
        });
      }
      return country ? country.name : "";
    }
    case('classification'):
      return classification_choices[investor[fieldName]];
    case('deals'): {
      return investor.deals.length;
    }
    default: {
      return investor[fieldName];
    }
  }
}


export const dealExtraFieldLabels = {
}

export const investorExtraFieldLabels = {
  deals: 'Deals',
}
