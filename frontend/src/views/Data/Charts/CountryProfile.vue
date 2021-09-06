<template>
  <ChartsContainer>
    <div class="country-profile-graph">
      Number of intentions per category of production according to implementation status
      <div class="sankey-wrapper">
        <svg id="sankey" />
      </div>
      <div class="legend">
        This figure lists the intention of investments per negotiation status. Please
        note: a deal may have more than one intention.
      </div>
    </div>
  </ChartsContainer>
</template>

<script>
  import {
    flat_intention_of_investment_map,
    implementation_status_choices,
  } from "$utils/choices";
  import ChartsContainer from "$views/Data/Charts/ChartsContainer";
  import { do_the_sank } from "$views/Data/Charts/country_profile_sankey";
  import { data_deal_query } from "$views/Data/query";

  export default {
    name: "CountryProfileGraphs",
    components: { ChartsContainer },
    metaInfo() {
      return { title: this.$t("Country profile graphs") };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.$store.dispatch("showContextBar", false);
      });
    },
    data() {
      return { deals: [] };
    },
    apollo: {
      deals: data_deal_query,
    },
    computed: {
      sankey_data() {
        let datanodes = new Set();
        let datalinks = {};

        this.deals.forEach((d) => {
          if (!d.current_implementation_status) return;
          datanodes.add(d.current_implementation_status);
          d.current_intention_of_investment.forEach((ivi) => {
            datanodes.add(ivi);
            datalinks[[d.current_implementation_status, ivi]] =
              datalinks[[d.current_implementation_status, ivi]] + 1 || 1;
          });
        });

        const nodes = [...datanodes].map((n) => ({
          id: n,
          name: implementation_status_choices[n] || flat_intention_of_investment_map[n],
        }));

        const links = Object.entries(datalinks).map(([k, v]) => {
          let [source, target] = k.split(",");
          return { source, target, value: v };
        });

        return { nodes, links };
      },
    },
    watch: {
      sankey_data(newV) {
        if (newV) {
          do_the_sank(newV);
        }
      },
    },
  };
</script>
<style lang="scss" scoped>
  .country-profile-graph {
    margin-top: 5rem;
  }
</style>

<style>
  /*.node rect {*/
  /*  fill-opacity: 0.9;*/
  /*  shape-rendering: crispEdges;*/
  /*}*/

  /*.node text {*/
  /*  pointer-events: none;*/
  /*  text-shadow: 0 1px 0 #fff;*/
  /*}*/

  .link {
    fill: none;
    stroke-opacity: 0.3;
  }

  .link:hover {
    stroke-opacity: 0.5;
  }
</style>
