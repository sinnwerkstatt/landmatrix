<template>
  <div>
    <table id="summary" class="table table-striped">
      <thead>
      <tr>
        <th>#</th>
        <th>Target country</th>
        <th style="width:183px">Top investors</th>
        <th>Intention of investment</th>
        <th>Negotiation status</th>
        <th>Implementation status</th>
        <th>Deal size in ha</th>
      </tr>
      </thead>
      <tbody v-if="deals">
      <tr v-for="deal in deals" :key="deal.id">
        <td><a :href="deal.id">{{deal.id}}</a></td>
        <td>{{deal.target_country.name}}</td>
        <td v-html="deal.top_investors.join('<br>')"></td>
        <td class="intention">
          <ul class="list-unstyled">
            <li v-for="intention in parseIntentionOfInvestment(deal)"
                v-html="intention"/>
          </ul>
        </td>
        <td>{{parseNegotiationStatus(deal)}}</td>
        <td>{{parseImplementationStatus(deal)}}</td>
        <td class="deal_size number">{{new Intl.NumberFormat().format(deal.deal_size)}}
        </td>
      </tr>
      </tbody>
      <tbody v-else>
      <tr>
        <td colspan="10">
          <div style="text-align: center; font-size: 1.4em;">Loading deals ...<span class="lm-spinner"></span> </div>
        </td>
      </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
  import store from "@/store";

  const slugify = require("slugify");

  export default {
    // name: 'Deal',
    // data() {
    //   return {
    //     deals: ,
    //   };
    // },
    computed: {
      deals() {
        return this.$store.state.deals;
      }
    },
    // created: function () {
    //   this.$http.get(`/newdeal/api/deals/`)
    //       .then(response => {
    //         this.deals = response.data.deals;
    //       });
    // },
    methods: {
      parseIntentionOfInvestment(deal) {
        if (!deal.intention_of_investment) return "";
        return deal.intention_of_investment.map((int) => {
          let intention = int.value;
          let slug = slugify(intention, {lower: true});
          return `<a href="/data/by-intention/${intention}/"
                      class="toggle-tooltip intention-icon ${slug}" title=""
                      data-original-title="${intention}"><span>${intention}</span></a>`
        }).sort();
      },
      parseNegotiationStatus(deal) {
        if (!deal.negotiation_status) return "";
        let neg_status = deal.negotiation_status[0]["value"];
        let category_map = {
          "Expression of interest": "Intended",
          "Under negotiation": "Intended",
          "Memorandum of understanding": "Intended",
          "Oral agreement": "Concluded",
          "Contract signed": "Concluded",
          "Negotiations failed": "Failed",
          "Contract canceled": "Failed",
          "Contract expired": "Failed",
          "Change of ownership": "",
        };
        if (neg_status === "Change of ownership") return neg_status;
        return `${category_map[neg_status]} (${neg_status})`;
      },
      parseImplementationStatus(deal) {
        if (!deal.implementation_status) return "";
        return deal.implementation_status[0]['value'];
      }
    },
    beforeRouteEnter(to, from, next) {
      store.dispatch('setTitle', "All Deals");
      store.dispatch('fetchDeals', {"offset": 0});
      next()
    },
  };
</script>
