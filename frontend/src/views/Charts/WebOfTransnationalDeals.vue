<template>
  <div class="">
    Web of Transnational deals and Global map of investments together O_O
    <div class="container" id="graph-div">
      <svg width="800"></svg>
    </div>
  </div>
</template>

<style scoped>
  h1 {
    text-align: center;
  }

  p {
    max-width: 1000px;
    margin: auto;
    text-align: justify;
  }

  #graph-div {
    text-align: center;
  }

  /* .node circle {
  fill: #999;
} */

  .node text {
    font: 10px sans-serif;
  }

  /* .node--internal circle {
  fill: #555;
} */

  .node--internal text {
    text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
  }

  .link {
    fill: none;
    stroke: #555;
    stroke-opacity: 0.4;
    stroke-width: 1.5px;
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
