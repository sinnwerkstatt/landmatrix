<template>
  <CountryProfileChartWrapper
    svg-id="sankey"
    :title="title"
    @downloadJSON="downloadJSON"
    @downloadCSV="downloadCSV"
  >
    <template slot="default">
      <svg id="sankey" />
    </template>
    <template slot="legend">
      {{ $t("This figure lists the intention of investments per negotiation status.") }}
      <br />
      {{ $t("Please note: a deal may have more than one intention.") }}<br />
      <i v-if="sankey_legend_numbers">
        {{
          $t(
            "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",
            sankey_legend_numbers
          )
        }}
      </i>
    </template>
  </CountryProfileChartWrapper>
</template>

<script lang="ts">
  import Vue from "vue";
  import type { PropType } from "vue";
  import { a_download, fileName } from "$utils/charts";
  import {
    flat_intention_of_investment_map,
    implementation_status_choices,
  } from "$utils/choices";
  import { LamaSankey, sankey_links_to_csv_cross } from "./intentions_per_category";
  import type { Deal } from "$types/deal";
  import CountryProfileChartWrapper from "$components/Charts/CountryProfile/CountryProfileChartWrapper.vue";

  export default Vue.extend({
    name: "IntentionsPerCategory",
    components: { CountryProfileChartWrapper },
    props: {
      deals: { type: [] as PropType<Deal[]>, required: true },
    },
    data() {
      return {
        title: this.$t(
          "Number of intentions per category of production according to implementation status"
        ).toString(),
        sankey: new LamaSankey(),
        sankey_links: [],
      };
    },
    computed: {
      sankey_legend_numbers(): { [key: string]: number } {
        if (this.deals.length === 0) return {};
        let multi_deal_count = this.deals.filter(
          (d) => d.current_intention_of_investment?.length > 1
        ).length;
        let all_intentions = this.deals
          .map((d) => d.current_intention_of_investment?.length || 0)
          .reduce((a, b) => a + b, 0);
        return { x: multi_deal_count, y: all_intentions, z: this.deals.length };
      },
    },
    watch: {
      deals() {
        if (!this.deals) return;
        let datanodes: Set<string> = new Set();
        let datalinks: { [key: string]: number } = {};

        let i_status_counter: { [key: string]: number } = {};

        this.deals.forEach((d: Deal) => {
          const i_stat = d.current_implementation_status ?? "S_UNKNOWN";
          const ivis = d.current_intention_of_investment ?? ["I_UNKNOWN"];

          datanodes.add(i_stat);
          i_status_counter[i_stat] = i_status_counter[i_stat] + 1 || 1;

          ivis.forEach((ivi) => {
            datanodes.add(ivi);
            datalinks[`${i_stat},${ivi}`] = datalinks[`${i_stat},${ivi}`] + 1 || 1;
          });
        });

        const nodes = [...datanodes].map((n) => {
          const istatus = implementation_status_choices[n] || n === "S_UNKNOWN";
          const deal_count = istatus ? i_status_counter[n] : 0;
          const name = this.$t(
            (n === "S_UNKNOWN" && "Status unknown") ||
              (n === "I_UNKNOWN" && "Intention unknown") ||
              implementation_status_choices[n] ||
              flat_intention_of_investment_map[n]
          ).toString();

          return { id: n, istatus, deal_count, name };
        });

        const links = Object.entries(datalinks).map(([k, v]) => {
          let [source, target] = k.split(",");
          return { source, target, value: v };
        });
        this.sankey_links = JSON.parse(JSON.stringify(links));
        if (this.sankey) this.sankey.do_the_sank("#sankey", { nodes, links });
      },
    },
    methods: {
      downloadJSON() {
        let data =
          "data:application/json;charset=utf-8," +
          encodeURIComponent(JSON.stringify(this.sankey_links, null, 2));
        a_download(data, fileName(this.title, ".json"));
      },
      downloadCSV() {
        const csv = sankey_links_to_csv_cross(this.sankey_links);
        let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
        a_download(data, fileName(this.title, ".csv"));
      },
    },
  });
</script>

<style lang="scss" scoped>
  .download-buttons {
    background: #2d2d2dff;
    color: var(--color-lm-light);
    border-radius: 0 0 5px 5px;

    button {
      color: var(--color-lm-light);
      font-size: 0.85rem;
      padding: 0 0.75rem 0.15rem;
    }
  }
</style>

<style lang="scss">
  #sankey .link:hover {
    stroke-opacity: 0.9;
  }
</style>
