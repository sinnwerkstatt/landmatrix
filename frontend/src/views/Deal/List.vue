<template>
  <div class="container">
    <div v-html="data_introduction"></div>
    <FilterBar />
    <table id="summary" class="table table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>Target country</th>
          <th style="width: 183px;">Top investors</th>
          <th>Intention of investment</th>
          <th>Negotiation status</th>
          <th>Implementation status</th>
          <th>Deal size in ha</th>
        </tr>
      </thead>
      <tbody v-if="deals">
        <tr v-for="deal in deals.slice(20*currentPage,20*(currentPage+1))" :key="deal.id">
          <td>
            <router-link :to="{ name: 'deal_detail', params: { deal_id: deal.id } }">
              {{ deal.id }}</router-link
            >
          </td>
          <td>{{ deal.target_country ? deal.target_country.name : "" }}</td>
          <td v-html="parseTopInvestors(deal)"></td>
          <td class="intention">
            <ul class="list-unstyled">
              <li
                v-for="intention in parseIntentionOfInvestment(deal)"
                v-html="intention"
              />
            </ul>
          </td>
          <td>{{ mapNegotiationStatus(deal) }}</td>
          <td>{{ mapImplementationStatus(deal) }}</td>
          <td class="deal_size number">
            {{ new Intl.NumberFormat().format(deal.deal_size) }}
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr>
          <td colspan="10">
            <div style="text-align: center; font-size: 1.4em;">
              Loading deals ...<span class="lm-spinner"></span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <div>
      <button @click="currentPage-=1">Zurueck</button>
      <button @click="currentPage+=1">Weiter</button>
    </div>
  </div>
</template>

<script>
  import FilterBar from "@/components/FilterBar";
  import store from "@/store";

  const slugify = require("slugify");

  export default {
    components: { FilterBar },
    data() {
      return {
        currentPage: 0,
      };
    },
    computed: {
      deals() {
        return this.$store.state.deals;
      },
      data_introduction() {
        if (this.$store.state.wagtailRootPage)
          return this.$store.state.wagtailRootPage.data_introduction;
      },
    },
    methods: {
      parseTopInvestors(deal) {
        if (!deal.top_investors) return "";
        return deal.top_investors
          .map((inv) => {
            return inv.name;
          })
          .join("<br>");
      },
      parseIntentionOfInvestment(deal) {
        if (!deal.intention_of_investment) return "";
        return deal.intention_of_investment
          .map((int) => {
            let intention = int.value;
            let slug = slugify(intention, { lower: true });
            return `<a href="/data/by-intention/${intention}/"
                      class="toggle-tooltip intention-icon ${slug}" title=""
                      data-original-title="${intention}"><span>${intention}</span></a>`;
          })
          .sort();
      },
      mapNegotiationStatus(deal) {
        return {
          10: "Expression of interest (Intended)",
          11: "Under negotiation (Intended)",
          12: "Memorandum of understanding (Intended)",
          20: "Oral agreement (Concluded)",
          21: "Contract signed (Concluded)",
          30: "Negotiations failed (Failed)",
          31: "Contract canceled (Failed)",
          32: "Contract expired (Failed)",
          40: "Change of ownership",
        }[deal.current_negotiation_status];
      },
      mapImplementationStatus(deal) {
        return {
          10: "Project not started",
          20: "Startup phase (no production)",
          30: "In operation (production)",
          40: "Project abandoned",
        }[deal.current_implementation_status];
      },
    },
    beforeRouteEnter(to, from, next) {
      let title = "All Deals";
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [{ link: { name: "wagtail" }, name: "Home" }, { name: title }],
      });
      next();
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";
  @import "../../scss/fonts";

  td {
    font-family: landmatrix;
  }
</style>
