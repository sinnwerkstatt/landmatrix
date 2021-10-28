<template>
  <CountryProfileChartWrapper
    svg-id="lslabyneg"
    :title="title"
    @downloadJSON="downloadJSON"
    @downloadCSV="downloadCSV"
  >
    <template slot="default">
      <svg id="lslabyneg" />
    </template>
    <template slot="legend"> Legende </template>
  </CountryProfileChartWrapper>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import CountryProfileChartWrapper from "$components/Charts/CountryProfile/CountryProfileChartWrapper.vue";
  import { LSLAByNegotiation } from "$components/Charts/CountryProfile/lsla_by_negotiation";
  import type { Deal } from "$types/deal";
  import {
    flat_negotiation_status_map,
    negotiation_status_group_map,
  } from "$utils/choices";

  export default Vue.extend({
    name: "LSLAByNegotiation",
    components: { CountryProfileChartWrapper },
    props: {
      deals: { type: [] as PropType<Deal[]>, required: true },
    },
    data() {
      return {
        title: this.$t("LSLA by negotiation status").toString(),
        svg: new LSLAByNegotiation(),
      };
    },
    watch: {
      deals() {
        if (!this.svg || !this.deals) return;
        const filter_negstat = this.$store.state.filters.filters.negotiation_status;
        const selected_neg_stat =
          filter_negstat.length > 0
            ? [...filter_negstat]
            : ["INTENDED", "CONCLUDED", "FAILED"];

        let pots: { [key: string]: { amount: number; size: number; meta?: boolean } } =
          {};
        if (selected_neg_stat.includes("INTENDED")) {
          pots.EXPRESSION_OF_INTEREST = { amount: 0, size: 0 };
          pots.UNDER_NEGOTIATION = { amount: 0, size: 0 };
          pots.MEMORANDUM_OF_UNDERSTANDING = { amount: 0, size: 0 };
          pots.INTENDED = { amount: 0, size: 0, meta: true };
        }
        if (selected_neg_stat.includes("CONCLUDED")) {
          pots.ORAL_AGREEMENT = { amount: 0, size: 0 };
          pots.CONTRACT_SIGNED = { amount: 0, size: 0 };

          pots.CONCLUDED = { amount: 0, size: 0, meta: true };
        }
        if (selected_neg_stat.includes("FAILED")) {
          pots.NEGOTIATIONS_FAILED = { amount: 0, size: 0 };
          pots.CONTRACT_CANCELED = { amount: 0, size: 0 };
          pots.FAILED = { amount: 0, size: 0, meta: true };
        }

        this.deals.forEach((d: Deal) => {
          const ngrp = negotiation_status_group_map[d.current_negotiation_status];
          // const name = this.$t(nstat.title).toString();
          pots[d.current_negotiation_status].amount += 1;
          pots[d.current_negotiation_status].size += d.current_contract_size || 0;
          if (ngrp) {
            pots[ngrp].amount += 1;
            pots[ngrp].size += d.current_contract_size || 0;
          }
        });

        this.svg.do_the_graph(
          "#lslabyneg",
          Object.entries(pots).map(([k, v]) => {
            const name = this.$t(flat_negotiation_status_map[k]).toString();
            return { name, ...v };
          })
        );
      },
    },
    methods: {
      downloadJSON() {
        // let data =
        //   "data:application/json;charset=utf-8," +
        //   encodeURIComponent(JSON.stringify(this.payload, null, 2));
        // a_download(data, fileName(this.title, ".json"));
      },
      downloadCSV() {
        // const csv = dynamics_csv(this.payload);
        // let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
        // a_download(data, fileName(this.title, ".csv"));
      },
    },
  });
</script>

<style lang="scss" scoped></style>
