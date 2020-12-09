import {
  implementation_status_choices,
  intention_of_investment_map,
  negotiation_status_map,
  classification_choices,
} from "/choices";
import dayjs from "dayjs";

export const getDealValue = function (component, deal, fieldName) {
  if (fieldName in deal) {
    switch (fieldName) {
      case "modified_at":
      case "created_at":
      case "fully_updated_at": {
        let date = deal[fieldName];
        return date ? dayjs(date).format("YYYY-MM-DD") : "";
      }
      case "id": {
        let location = { name: "deal_detail", params: { deal_id: deal.id } };
        let url = component.$router.resolve(location).href;
        // TODO: Turn this into a router-link. Beware: you can't just replace it here.
        return `<a class="label label-deal" href="${url}">${deal.id}</a>`;
      }
      case "deal_size":
        return deal.deal_size ? deal.deal_size.toLocaleString() + " ha" : "";
      case "intended_size":
        return deal.intended_size ? deal.intended_size.toLocaleString() + " ha" : "";

      case "operating_company": {
        if (deal.operating_company) {
          let investor_id = deal.operating_company.id;
          if (investor_id) {
            let location = { name: "investor_detail", params: { investor_id } };
            let url = component.$router.resolve(location).href;
            return `<a class="investor" target="_blank" href="${url}">${deal.operating_company.name}</a>`;
          }
        }
        return "";
      }

      case "top_investors": {
        if (deal.top_investors) {
          return deal.top_investors
            .map((i) => {
              let location = { name: "investor_detail", params: { investor_id: i.id } };
              let url = component.$router.resolve(location).href;
              return `<a class="investor" target="_blank" href="${url}">${i.name}</a>`;
            })
            .join("<br/>");
        }
        return "";
      }

      case "country": {
        let country = component.$store.getters.getCountryOrRegion({
          type: "country",
          id: deal.country.id,
        });
        return country ? country.name : "";
      }
      case "intention_of_investment": {
        let intentions;
        if (deal.current_intention_of_investment) {
          intentions = deal.current_intention_of_investment
            .map((ioi) => {
              let [intention, icon] = intention_of_investment_map[ioi];
              return `<span class="ioi-label"><i class="${icon}"></i> ${component.$t(
                intention
              )}</span>`;
            })
            .join(" ");
        }
        return intentions;
      }
      case "current_negotiation_status": {
        //TODO: Why is there deals with current_negotiation_status === null?
        let [neg_status, neg_status_group] = ["UNDEFINED", null];
        if (deal.current_negotiation_status) {
          [neg_status, neg_status_group] = negotiation_status_map[
            deal.current_negotiation_status
          ];
        }
        return neg_status_group ? `${neg_status_group} (${neg_status})` : neg_status;
      }
      case "current_implementation_status": {
        return deal.current_implementation_status
          ? implementation_status_choices[deal.current_implementation_status]
          : "None";
      }
      default: {
        return deal[fieldName];
      }
    }
  } else {
    return "";
  }
};

export const getInvestorValue = function (component, investor, fieldName) {
  switch (fieldName) {
    case "modified_at":
    case "created_at": {
      let date = investor[fieldName];
      return date ? dayjs(date).format("YYYY-MM-DD") : "";
    }
    case "id": {
      let location = { name: "investor_detail", params: { investor_id: investor.id } };
      let url = component.$router.resolve(location).href;
      return `<a class="label label-investor" href="${url}">${investor.id}</a>`;
    }
    case "country": {
      let country = null;
      if (investor.country) {
        if (investor.country.name) {
          return investor.country.name;
        } else {
          country = component.$store.getters.getCountryOrRegion({
            type: "country",
            id: investor.country.id,
          });
        }
      }
      return country ? country.name : "";
    }
    case "classification":
      return classification_choices[investor[fieldName]];
    case "deals": {
      return investor.deals.length;
    }
    default: {
      return investor[fieldName];
    }
  }
};

export const dealExtraFieldLabels = {
  modified_at: "Last modified",
  fully_updated_at: "Last full update",
  top_investors: "Top investors", // TODO: should come from formFields!
};

export const investorExtraFieldLabels = {
  modified_at: "Last modified",
  deals: "Deals",
};
