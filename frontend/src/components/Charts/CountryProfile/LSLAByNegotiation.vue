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
    <!--    <template slot="legend"> Legende </template>-->
  </CountryProfileChartWrapper>
</template>

<script lang="ts">
  import CountryProfileChartWrapper from "$components/Charts/CountryProfile/CountryProfileChartWrapper.vue";
  import {
    LSLAByNegotiation,
    LSLAData,
  } from "$components/Charts/CountryProfile/lsla_by_negotiation";
  import type { Deal } from "$types/deal";
  import { negotiation_status_group_map } from "$utils/choices";
  import Vue from "vue";
  import type { PropType } from "vue";

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
        const filter_negstat = this.$store.state.filters.negotiation_status;
        const selected_neg_stat =
          filter_negstat.length > 0
            ? [...filter_negstat]
            : [
                "EXPRESSION_OF_INTEREST",
                "UNDER_NEGOTIATION",
                "MEMORANDUM_OF_UNDERSTANDING",
                "ORAL_AGREEMENT",
                "CONTRACT_SIGNED",
                "CHANGE_OF_OWNERSHIP",
                "NEGOTIATIONS_FAILED",
                "CONTRACT_CANCELED",
                "CONTRACT_EXPIRED",
              ];

        let pots: { [key: string]: LSLAData } = {};
        if (selected_neg_stat.includes("EXPRESSION_OF_INTEREST"))
          pots.EXPRESSION_OF_INTEREST = new LSLAData("EXPRESSION_OF_INTEREST");
        if (selected_neg_stat.includes("UNDER_NEGOTIATION"))
          pots.UNDER_NEGOTIATION = new LSLAData("UNDER_NEGOTIATION");
        if (selected_neg_stat.includes("MEMORANDUM_OF_UNDERSTANDING"))
          pots.MEMORANDUM_OF_UNDERSTANDING = new LSLAData(
            "MEMORANDUM_OF_UNDERSTANDING"
          );
        if (
          selected_neg_stat.includes("EXPRESSION_OF_INTEREST") &&
          selected_neg_stat.includes("UNDER_NEGOTIATION") &&
          selected_neg_stat.includes("MEMORANDUM_OF_UNDERSTANDING")
        )
          pots.INTENDED = new LSLAData("INTENDED", true);
        if (selected_neg_stat.includes("ORAL_AGREEMENT"))
          pots.ORAL_AGREEMENT = new LSLAData("ORAL_AGREEMENT");
        if (selected_neg_stat.includes("CONTRACT_SIGNED"))
          pots.CONTRACT_SIGNED = new LSLAData("CONTRACT_SIGNED");
        if (selected_neg_stat.includes("CHANGE_OF_OWNERSHIP"))
          pots.CHANGE_OF_OWNERSHIP = new LSLAData("CHANGE_OF_OWNERSHIP");
        if (
          selected_neg_stat.includes("ORAL_AGREEMENT") &&
          selected_neg_stat.includes("CONTRACT_SIGNED") &&
          selected_neg_stat.includes("CHANGE_OF_OWNERSHIP")
        )
          pots.CONCLUDED = new LSLAData("CONCLUDED", true);
        if (selected_neg_stat.includes("NEGOTIATIONS_FAILED"))
          pots.NEGOTIATIONS_FAILED = new LSLAData("NEGOTIATIONS_FAILED");
        if (selected_neg_stat.includes("CONTRACT_CANCELED"))
          pots.CONTRACT_CANCELED = new LSLAData("CONTRACT_CANCELED");
        if (
          selected_neg_stat.includes("NEGOTIATIONS_FAILED") &&
          selected_neg_stat.includes("CONTRACT_CANCELED")
        )
          pots.FAILED = new LSLAData("FAILED", true);
        if (selected_neg_stat.includes("CONTRACT_EXPIRED"))
          pots.CONTRACT_EXPIRED = new LSLAData("CONTRACT_EXPIRED", true);

        this.deals.forEach((d: Deal) => {
          if (!d.current_negotiation_status) return;
          (pots[d.current_negotiation_status] as LSLAData).add(
            d.current_contract_size,
            d.intended_size
          );
          const ngrp = negotiation_status_group_map[d.current_negotiation_status];
          if (ngrp && pots[ngrp])
            (pots[ngrp] as LSLAData).add(d.current_contract_size, d.intended_size);
        });

        this.svg.do_the_graph("#lslabyneg", Object.values(pots));
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
