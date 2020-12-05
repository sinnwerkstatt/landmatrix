<template>
  <div>
    <h2 class="bar-title">Web of transnational deals</h2>
    <div v-html="chart_desc" />
    <div v-if="country" class="hint-box">
      <h4>{{ country.name }}</h4>
      <!--      <div class="mx-3">-->
      <!--        <b-->
      <!--          class="deal-ranking"-->
      <!--          v-if="this.country_investments_and_rankings.ranking_deal"-->
      <!--        >-->
      <!--          <i class="fas fa-compress-arrows-alt"></i> #{{-->
      <!--            this.country_investments_and_rankings.ranking_deal-->
      <!--          }}-->
      <!--        </b>-->
      <!--        &nbsp;-->
      <!--        <b-->
      <!--          class="investor-ranking"-->
      <!--          v-if="this.country_investments_and_rankings.ranking_investor"-->
      <!--        >-->
      <!--          <i class="fas fa-expand-arrows-alt"></i> #{{-->
      <!--            this.country_investments_and_rankings.ranking_investor-->
      <!--          }}-->
      <!--        </b>-->
      <!--      </div>-->
      <div v-if="investing_countries.length > 0">
        <b>Countries investing in {{ country.name }}</b>
        <table class="table-striped">
          <tbody>
            <tr v-for="icountry in investing_countries">
              <th>{{ icountry.country_name }}</th>
              <td>
                {{ icountry.count }} deals<br />
                {{ icountry.size }} ha
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="invested_countries.length > 0">
        <b>Countries {{ country.name }} invests in</b>
        <table class="table-striped">
          <tbody>
            <tr v-for="icountry in invested_countries">
              <th>{{ icountry.country_name }}</th>
              <td>
                {{ icountry.count }} deals<br />
                {{ icountry.size }} ha
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="hint-box">
      <h4>{{ $t("Global ranking") }}</h4>
      <div v-if="global_rankings">
        <b><i class="fas fa-compress-arrows-alt"></i> Top invested-in Countries</b>
        <table class="table-striped">
          <tbody>
            <tr v-for="rank in global_ranking_deals">
              <th>{{ rank.country_name }}</th>
              <td>{{ rank.deal_size__sum.toLocaleString() }} ha</td>
            </tr>
          </tbody>
        </table>

        <b><i class="fas fa-expand-arrows-alt"></i> Top investing Countries</b>
        <table class="table-striped">
          <tbody>
            <tr v-for="rank in global_ranking_investors">
              <th>{{ rank.country_name }}</th>
              <td>{{ rank.deal_size__sum.toLocaleString() }} ha</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import gql from "graphql-tag";
  import { mapGetters } from "vuex";

  export default {
    name: "ContextBarWebOfTransnationalDeals",
    props: ["filters"],
    apollo: {
      global_rankings: gql`
        query {
          global_rankings
        }
      `,
      country_investments_and_rankings: {
        query: gql`
          query InvestmentsAndRankings($id: Int!, $filters: [Filter]) {
            country_investments_and_rankings(id: $id, filters: $filters)
          }
        `,
        variables() {
          return {
            id: +this.country_id,
            filters: this.filters,
          };
        },
        skip() {
          return !this.country_id;
        },
      },
    },
    data() {
      return {
        global_rankings: null,
        country_investments_and_rankings: {
          investing: [],
          invested: [],
          ranking_deal: null,
          ranking_investor: null,
        },
      };
    },
    computed: {
      ...mapGetters(["getCountryOrRegion"]),
      country_id() {
        return this.$store.state.filters.filters.country_id;
      },
      chart_desc() {
        if (!this.$store.state.page.chartDescriptions) return null;
        return this.$store.state.page.chartDescriptions.web_of_transnational_deals;
      },
      country() {
        if (!this.country_id || this.country_id === 0) return null;
        return this.getCountryOrRegion({
          id: this.country_id,
        });
      },
      investing_countries() {
        return this.country_investments_and_rankings.investing.map((x) => {
          let country_name = this.getCountryOrRegion({
            id: +x.country_id,
          }).name;
          return { country_name, ...x };
        });
      },
      invested_countries() {
        return this.country_investments_and_rankings.invested.map((x) => {
          let country_name = this.getCountryOrRegion({
            id: +x.country_id,
          }).name;
          return { country_name, ...x };
        });
      },
      global_ranking_deals() {
        if (!this.global_rankings) return;
        if (this.$store.state.page.countries.length === 0) return;
        return this.global_rankings.ranking_deal.map((x) => {
          let country_name = this.getCountryOrRegion({
            id: +x.country_id,
          }).name;
          return { country_name, ...x };
        });
      },
      global_ranking_investors() {
        if (!this.global_rankings) return;
        if (this.$store.state.page.countries.length === 0) return;
        return this.global_rankings.ranking_investor.map((x) => {
          let country_name = this.getCountryOrRegion({
            id: +x.country_id,
          }).name;
          return { country_name, ...x };
        });
      },
    },
  };
</script>

<style lang="scss">
  @import "src/scss/colors";

  .investor-ranking {
    color: $primary;
  }
  .deal-ranking {
    color: $lm_investor;
  }

  .hint-box {
    padding: 1em;
    font-size: 0.9em;
    margin-bottom: 20px;
    background-color: #f5f5f5;
    border: 1px solid #e3e3e3;
    border-radius: 4px;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
  }
</style>
<style lang="scss" scoped>
  b {
    padding: 3px;
    display: inline-block;
  }
  table {
    width: 100%;
  }

  th {
    text-align: left;
  }

  td {
    text-align: right;
    white-space: nowrap;
  }
</style>
