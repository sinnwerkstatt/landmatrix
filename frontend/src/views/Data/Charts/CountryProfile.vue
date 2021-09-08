<template>
  <ChartsContainer>
    <div class="country-profile-graph">
      <h2>
        Number of intentions per category of production according to implementation
        status
      </h2>
      <div class="sankey-wrapper">
        <svg id="sankey" />
      </div>
      <div class="legend">
        {{
          $t("This figure lists the intention of investments per negotiation status.")
        }}
        <br />
        {{ $t("Please note: a deal may have more than one intention.") }}<br />
        <i
          >{{
            $t(
              "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",
              sankey_legend_numbers
            )
          }}
        </i>
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
  import { LamaSankey } from "$views/Data/Charts/country_profile_sankey";
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
      return { deals: [], sankey: null };
    },
    apollo: {
      deals: data_deal_query,
    },
    computed: {
      sankey_legend_numbers() {
        let multi_deal_count = this.deals.filter(
          (d) => d.current_intention_of_investment.length > 1
        ).length;
        let all_intentions = this.deals
          .map((d) => d.current_intention_of_investment.length)
          .reduce((a, b) => a + b, 0);
        return { x: multi_deal_count, y: all_intentions, z: this.deals.length };
      },
    },
    watch: {
      deals() {
        if (!this.deals) return;
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

        const nodes = [...datanodes].map((n) => {
          return {
            id: n,
            ivi: !implementation_status_choices[n],
            name:
              implementation_status_choices[n] || flat_intention_of_investment_map[n],
          };
        });

        const links = Object.entries(datalinks).map(([k, v]) => {
          let [source, target] = k.split(",");
          return { source, target, value: v };
        });

        this.sankey.do_the_sank({ nodes, links });
      },
    },
    mounted() {
      this.sankey = new LamaSankey("#sankey");
    },
  };
</script>
<style lang="scss" scoped>
  .country-profile-graph {
    width: 600px;
    margin-top: 5rem;
  }
</style>

<style lang="scss">
  .sankey-wrapper {
    .node rect {
      /*fill-opacity: 0.9;*/
      shape-rendering: crispEdges;
      cursor: move;
    }

    .node text {
      cursor: move;
      text-shadow: 0 1px 0 #fff;
    }

    .link {
      fill: none;
      stroke-opacity: 0.3;
    }

    .link:hover {
      stroke-opacity: 0.5;
    }
  }
</style>
