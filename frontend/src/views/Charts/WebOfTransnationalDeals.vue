<template>
  <div>
    <div class="container" id="graph-div">
      <svg width="800"></svg>
    </div>
  </div>
</template>

<style lang="scss">
  #graph-div {
    text-align: center;
    .link {
      fill: none;
      stroke: #555;
      stroke-opacity: 0.4;
      stroke-width: 4.5px;
    }
    svg {
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

  export default {
    name: "Charts",
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
        LandMatrixRadialSpider(this.transnational_deals, "svg");
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
