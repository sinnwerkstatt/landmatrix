<template>
  <div>
    <h2 class="bar-title">Web of transnational deals</h2>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <div v-html="chart_description" />
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
        <b>{{ $t("Countries investing in {country}", { country: country.name }) }}</b>
        <table class="table-striped">
          <tbody>
            <tr v-for="icountry in investing_countries" :key="icountry.country_name">
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
            <tr v-for="icountry in invested_countries" :key="icountry.country_name">
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
    <!--    <div v-else class="hint-box">-->
    <!--      <h4>{{ $t("Global ranking") }}</h4>-->
    <!--      <div v-if="global_rankings">-->
    <!--        <b><i class="fas fa-compress-arrows-alt"></i> Top invested-in Countries</b>-->
    <!--        <table class="table-striped">-->
    <!--          <tbody>-->
    <!--            <tr v-for="rank in global_ranking_deals">-->
    <!--              <th>{{ rank.country_name }}</th>-->
    <!--              <td>{{ rank.deal_size__sum.toLocaleString() }} ha</td>-->
    <!--            </tr>-->
    <!--          </tbody>-->
    <!--        </table>-->

    <!--        <b><i class="fas fa-expand-arrows-alt"></i> Top investing Countries</b>-->
    <!--        <table class="table-striped">-->
    <!--          <tbody>-->
    <!--            <tr v-for="rank in global_ranking_investors">-->
    <!--              <th>{{ rank.country_name }}</th>-->
    <!--              <td>{{ rank.deal_size__sum.toLocaleString() }} ha</td>-->
    <!--            </tr>-->
    <!--          </tbody>-->
    <!--        </table>-->
    <!--      </div>-->
    <!--    </div>-->
  </div>
</template>

<script lang="ts">
  import gql from "graphql-tag";
  import Vue from "vue";
  import type { Country, CountryOrRegion } from "$types/wagtail";

  export default Vue.extend({
    name: "ContextBarWebOfTransnationalDeals",
    props: {
      filters: { type: Array, required: true },
    },
    apollo: {
      global_rankings: {
        query: gql`
          query GlobalRankings($filters: [Filter]) {
            global_rankings(filters: $filters)
          }
        `,
        variables() {
          return {
            filters: this.$store.getters.defaultFiltersForGQL,
          };
        },
      },
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
      getCountryOrRegion(): CountryOrRegion {
        return this.$store.getters.getCountryOrRegion;
      },
      country_id(): number | null {
        return this.$store.state.filters.country_id;
      },
      chart_description(): null | string {
        if (!this.$store.state.chartDescriptions) return null;
        // noinspection JSUnresolvedVariable
        return this.$store.state.chartDescriptions.web_of_transnational_deals;
      },
      country(): Country | null {
        if (!this.country_id || this.country_id === 0) return null;
        return this.getCountryOrRegion({
          id: this.country_id,
        });
      },
      investing_countries(): Country[] {
        return this.country_investments_and_rankings.investing.map((x) => {
          let country_name = this.getCountryOrRegion({
            id: +x.country_id,
          }).name;
          return { country_name, ...x };
        });
      },
      invested_countries(): Country[] {
        return this.country_investments_and_rankings.invested.map((x) => {
          let country_name = this.getCountryOrRegion({
            id: +x.country_id,
          }).name;
          return { country_name, ...x };
        });
      },
      // global_ranking_deals() {
      //   if (!this.global_rankings) return;
      //   if (this.$store.state.countries.length === 0) return;
      //   return this.global_rankings.ranking_deal.map((x) => {
      //     let country_name = this.getCountryOrRegion({
      //       id: +x.country_id,
      //     }).name;
      //     return { country_name, ...x };
      //   });
      // },
      // global_ranking_investors() {
      //   if (!this.global_rankings) return;
      //   if (this.$store.state.countries.length === 0) return;
      //   return this.global_rankings.ranking_investor.map((x) => {
      //     let country_name = this.getCountryOrRegion({
      //       id: +x.country_id,
      //     }).name;
      //     return { country_name, ...x };
      //   });
      // },
    },
  });
</script>

<style lang="scss">
  //.investor-ranking {
  //  color: var(--color-lm-orange);
  //}
  //.deal-ranking {
  //  color: var(--color-lm-investor);
  //}

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
