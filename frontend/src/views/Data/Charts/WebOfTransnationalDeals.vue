<template>
  <ChartsContainer>
    <template v-slot:default>
      <LoadingPulse v-if="$apollo.queries.transnational_deals.loading" />
      <div id="svg-container">
        <svg></svg>
      </div>
    </template>
    <template v-slot:ContextBar>
      <ContextBarWebOfTransnationalDeals />
    </template>
  </ChartsContainer>
</template>

<script>
  import ChartsContainer from "./ChartsContainer";
  import { LandMatrixRadialSpider } from "./d3_hierarchical_edge_bundling";
  import gql from "graphql-tag";
  import LoadingPulse from "/components/Data/LoadingPulse";
  import ContextBarWebOfTransnationalDeals from "/components/Charts/ContextBarWebOfTransnationalDeals";

  export default {
    name: "WebOfTransnationalDeals",
    props: ["changeDeal"],
    components: { ChartsContainer, LoadingPulse, ContextBarWebOfTransnationalDeals },
    apollo: {
      transnational_deals: gql`
        query {
          transnational_deals
        }
      `
    },
    data() {
      return {
        transnational_deals: []
      };
    },
    watch: {
      transnational_deals() {
        LandMatrixRadialSpider(this.transnational_deals, "#svg-container > svg", (country) => {
          this.$store.dispatch("selectChartSelectedCountry", country);
        });
      }
    }
  };
</script>
<style lang="scss">
  //.link {
  //  fill: none;
  //  stroke: #555;
  //  stroke-opacity: 0.4;
  //  stroke-width: 4.5px;
  //}

  #svg-container {
    width: 100%;
    align-self: safe center;
    > svg {
      text {
        font-size: 14px;
        cursor: pointer;
      }
    }
  }
</style>
