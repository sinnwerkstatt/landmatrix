<template>
  <ChartsContainer>
    <LoadingPulse v-if="$apollo.queries.transnational_deals.loading" />
    <svg id="svgweb" width="800"></svg>
  </ChartsContainer>
</template>

<script>
  import ChartsContainer from "./ChartsContainer";
  import { LandMatrixRadialSpider } from "./d3_hierarchical_edge_bundling";
  import gql from "graphql-tag";
  import LoadingPulse from "/components/Data/LoadingPulse";

  export default {
    name: "WebOfTransnationalDeals",
    props: ["changeDeal"],
    components: { ChartsContainer, LoadingPulse },
    apollo: {
      transnational_deals: gql`
        query {
          transnational_deals
        }
      `,
    },
    data() {
      return {
        transnational_deals: [],
      };
    },
    watch: {
      transnational_deals() {
        LandMatrixRadialSpider(this.transnational_deals, "#svgweb", (country) => {
          this.$store.dispatch("selectChartSelectedCountry", country);
        });
      },
    },
  };
</script>
<style lang="scss">
  //.link {
  //  fill: none;
  //  stroke: #555;
  //  stroke-opacity: 0.4;
  //  stroke-width: 4.5px;
  //}

  #svgweb {
    text {
      font-size: 14px;
      cursor: pointer;
    }
  }
</style>
