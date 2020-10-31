<template>
  <div style="height: 100%;">
    <LoadingPulse v-if="$apollo.queries.transnational_deals.loading" />
    <div id="svg-container">
      <svg id="svgweb" width="800"></svg>
    </div>
  </div>
</template>

<style lang="scss">
  #svg-container {
    text-align: center;
    height: 100%;
    display: flex;
    justify-content: center;
    .link {
      fill: none;
      stroke: #555;
      stroke-opacity: 0.4;
      stroke-width: 4.5px;
    }
    #svgweb {
      text {
        font-size: 14px;
      }
    }
  }
</style>
<script>
  import store from "/store";
  import { LandMatrixRadialSpider } from "./d3_hierarchical_edge_bundling";
  import gql from "graphql-tag";
  import LoadingPulse from "/components/Data/LoadingPulse";

  export default {
    name: "WebOfTransnationalDeals",
    components: { LoadingPulse },
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
    beforeRouteEnter(to, from, next) {
      let title = "Web of transnational deals";
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "charts" }, name: "Charts" },
          { name: title },
        ],
      });
      next();
    },
    watch: {
      transnational_deals() {
        LandMatrixRadialSpider(this.transnational_deals, "#svgweb");
      },
    },
    // mounted() {
    //   // if (this.transnational_deals.length) {
    //   //   LandMatrixRadialSpider(this.transnational_deals, "svg");
    //   // }
    // }
  };
</script>

<style scoped></style>
