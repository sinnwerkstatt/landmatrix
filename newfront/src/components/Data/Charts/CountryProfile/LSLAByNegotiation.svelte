<script lang="ts">
  import { _ } from "svelte-i18n";
  import { browser } from "$app/env";
  import { deals } from "$lib/data";
  import { filters, NegotiationStatus } from "$lib/filters";
  import { negotiation_status_group_map } from "$components/Fields/Display/choices";
  import CountryProfileChartWrapper from "./CountryProfileChartWrapper.svelte";
  import { LSLAByNegotiation, LSLAData } from "./lsla_by_negotiation";

  let title = $_("LSLA by negotiation status");
  let svg = new LSLAByNegotiation();

  $: if (browser && $deals && $deals.length > 0) {
    const filter_negstat = $filters.negotiation_status;
    const selected_neg_stat =
      filter_negstat.length > 0
        ? [...filter_negstat]
        : [
            NegotiationStatus.EXPRESSION_OF_INTEREST,
            NegotiationStatus.UNDER_NEGOTIATION,
            NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING,
            NegotiationStatus.ORAL_AGREEMENT,
            NegotiationStatus.CONTRACT_SIGNED,
            NegotiationStatus.NEGOTIATIONS_FAILED,
            NegotiationStatus.CONTRACT_CANCELED,
            NegotiationStatus.CONTRACT_EXPIRED,
            NegotiationStatus.CHANGE_OF_OWNERSHIP,
          ];
    let pots: { [key: string]: LSLAData } = {};
    if (selected_neg_stat.includes(NegotiationStatus.EXPRESSION_OF_INTEREST))
      pots.EXPRESSION_OF_INTEREST = new LSLAData(
        NegotiationStatus.EXPRESSION_OF_INTEREST
      );
    if (selected_neg_stat.includes(NegotiationStatus.UNDER_NEGOTIATION))
      pots.UNDER_NEGOTIATION = new LSLAData(NegotiationStatus.UNDER_NEGOTIATION);
    if (selected_neg_stat.includes(NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING))
      pots.MEMORANDUM_OF_UNDERSTANDING = new LSLAData(
        NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING
      );
    if (
      selected_neg_stat.includes(NegotiationStatus.EXPRESSION_OF_INTEREST) &&
      selected_neg_stat.includes(NegotiationStatus.UNDER_NEGOTIATION) &&
      selected_neg_stat.includes(NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING)
    )
      pots.INTENDED = new LSLAData("INTENDED", true);
    if (selected_neg_stat.includes(NegotiationStatus.ORAL_AGREEMENT))
      pots.ORAL_AGREEMENT = new LSLAData(NegotiationStatus.ORAL_AGREEMENT);
    if (selected_neg_stat.includes(NegotiationStatus.CONTRACT_SIGNED))
      pots.CONTRACT_SIGNED = new LSLAData(NegotiationStatus.CONTRACT_SIGNED);
    if (
      selected_neg_stat.includes(NegotiationStatus.ORAL_AGREEMENT) &&
      selected_neg_stat.includes(NegotiationStatus.CONTRACT_SIGNED)
    )
      pots.CONCLUDED = new LSLAData("CONCLUDED", true);
    if (selected_neg_stat.includes(NegotiationStatus.NEGOTIATIONS_FAILED))
      pots.NEGOTIATIONS_FAILED = new LSLAData(NegotiationStatus.NEGOTIATIONS_FAILED);
    if (selected_neg_stat.includes(NegotiationStatus.CONTRACT_CANCELED))
      pots.CONTRACT_CANCELED = new LSLAData(NegotiationStatus.CONTRACT_CANCELED);
    if (
      selected_neg_stat.includes(NegotiationStatus.NEGOTIATIONS_FAILED) &&
      selected_neg_stat.includes(NegotiationStatus.CONTRACT_CANCELED)
    )
      pots.FAILED = new LSLAData("FAILED", true);
    if (selected_neg_stat.includes(NegotiationStatus.CONTRACT_EXPIRED))
      pots.CONTRACT_EXPIRED = new LSLAData(NegotiationStatus.CONTRACT_EXPIRED, true);
    if (selected_neg_stat.includes(NegotiationStatus.CHANGE_OF_OWNERSHIP))
      pots.CHANGE_OF_OWNERSHIP = new LSLAData(
        NegotiationStatus.CHANGE_OF_OWNERSHIP,
        true
      );

    $deals.forEach((d) => {
      if (!d.current_negotiation_status) return;
      (pots[d.current_negotiation_status] as LSLAData).add(
        d.current_contract_size,
        d.intended_size
      );
      const ngrp = negotiation_status_group_map[d.current_negotiation_status];
      if (ngrp && pots[ngrp])
        (pots[ngrp] as LSLAData).add(d.current_contract_size, d.intended_size);
    });

    svg.do_the_graph("#lslabyneg", Object.values(pots));
  }

  function downloadJSON() {
    // let data =
    //   "data:application/json;charset=utf-8," +
    //   encodeURIComponent(JSON.stringify(this.payload, null, 2));
    // a_download(data, fileName(this.title, ".json"));
  }
  function downloadCSV() {
    // const csv = dynamics_csv(this.payload);
    // let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
    // a_download(data, fileName(this.title, ".csv"));
  }
</script>

<CountryProfileChartWrapper
  svgID="lslabyneg"
  {title}
  on:downloadJSON={downloadJSON}
  on:downloadCSV={downloadCSV}
>
  <svg id="lslabyneg" />

  <!--    <template slot="legend"> Legende </template>-->
</CountryProfileChartWrapper>
