<template>
  <div>
    <h2 class="bar-title">Web of transnational deals</h2>
    <p>
      This interactive graph shows the global flow of transnational land acquisitions.
    </p>
    <p>
      Country names marked with * have been shortened to improve readability.
    </p>
    <div v-if="country" class="hint-box">
      <h4>{{ country.name }}</h4>
      <h5>Regions investing in {{ country.name }}</h5>
      <div v-html="investors"></div>
      <br />
      Show all inbound deals

      <h5>Regions {{ country.name }} invests in</h5>
      <div v-html="ventures"></div>
      <br />
      Show all outbound deals

      <h5>Global Deal Size Rank thingy</h5>
      This deal is on place #4<br />
    </div>
    <div v-else class="hint-box">
      <h4>World information</h4>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import gql from "graphql-tag";

  export default {
    name: "ContextBarCharts",
    apollo: {
      country_investments: {
        query: gql`
          query Investments($id: Int!) {
            country_investments(id: $id)
          }
        `,
        variables() {
          return {
            id: +this.country_id
          };
        },
        skip() {
          return !this.country_id;
        }
      }
    },
    data() {
      return {
        country_investments: null
      };
    },
    computed: {
      country_id() {
        return this.$store.state.filters.filters.country_id
      },
      country() {
        if (!this.country_id || this.country_id === 0) return null;
        return this.$store.getters.getCountryOrRegion({
          type: "country",
          id: this.country_id
        });
      },
      investors() {
        if (!this.country_investments) return;
        if (!this.country_investments.investing) return;
        let retdings = "<table><tbody>";
        Object.entries(this.country_investments.investing).forEach(([k, v]) => {
          let reg_name = this.$store.getters.getCountryOrRegion({
            type: "region",
            id: +k
          }).name;
          retdings += `<tr><th>${reg_name}</th><td>${v.size} ha (${v.count} deals)</td></tr>`;
        });
        retdings += "</tbody></table>";
        return retdings;
      },
      ventures() {
        if (!this.country_investments) return;
        if (!this.country_investments.invested) return;
        let retdings = "<table><tbody>";
        Object.entries(this.country_investments.invested).forEach(([k, v]) => {
          let reg_name = this.$store.getters.getCountryOrRegion({
            type: "region",
            id: +k
          }).name;
          retdings += `<tr><th>${reg_name}</th><td>${v.size} ha (${v.count} deals)</td></tr>`;
        });
        retdings += "</tbody></table>";
        return retdings;
      }
    }
  };
</script>

<style lang="scss">
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
