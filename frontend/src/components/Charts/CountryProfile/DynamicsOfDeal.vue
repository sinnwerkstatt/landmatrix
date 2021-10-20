<template>
  <CountryProfileChartWrapper
    svg-id="dynamicsofdeal"
    :title="title"
    @downloadJSON="downloadJSON"
    @downloadCSV="downloadCSV"
  >
    <template slot="default">
      <svg id="dynamicsofdeal" />
    </template>

    <template slot="legend">
      {{
        $t(
          "Please note: {number} deals have multiple investor types. The full size of the deal is assigned to each investor type.",
          { number: multideals }
        )
      }}
    </template>
  </CountryProfileChartWrapper>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import CountryProfileChartWrapper from "$components/Charts/CountryProfile/CountryProfileChartWrapper.vue";
  import {
    dynamics_csv,
    DynamicsDataPoint,
    DynamicsOfDeal,
  } from "$components/Charts/CountryProfile/dynamics_of_deal";
  import { classification_choices } from "$utils/choices";
  import type { Deal } from "$types/deal";
  import { a_download, fileName } from "$utils/charts";

  export default Vue.extend({
    name: "DynamicsOfDeal",
    components: { CountryProfileChartWrapper },
    props: {
      deals: { type: [] as PropType<Deal[]>, required: true },
    },
    data() {
      return {
        title: this.$t("Dynamics of deal by investor type").toString(),
        svg: new DynamicsOfDeal(),
        multideals: 0,
        payload: [] as DynamicsDataPoint[],
      };
    },
    watch: {
      deals() {
        if (!this.svg || !this.deals) return;
        let pots: { [key: string]: number } = {};
        this.deals.forEach((d: Deal) => {
          if (d.top_investors.length > 1) this.multideals += 1;
          d.top_investors.forEach((i) => {
            const cl = i.classification;
            pots[cl] = pots[cl] ? pots[cl] + d.deal_size : d.deal_size;
          });
        });

        this.payload = Object.entries(pots).map(([k, v]) => ({
          name: this.$t(classification_choices[k] || "Unknown").toString(),
          value: v,
        }));

        this.svg.do_the_graph("#dynamicsofdeal", this.payload);
      },
    },
    methods: {
      downloadJSON() {
        let data =
          "data:application/json;charset=utf-8," +
          encodeURIComponent(JSON.stringify(this.payload, null, 2));
        a_download(data, fileName(this.title, ".json"));
      },
      downloadCSV() {
        const csv = dynamics_csv(this.payload);
        let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
        a_download(data, fileName(this.title, ".csv"));
      },
    },
  });
</script>
