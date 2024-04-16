<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import { LSLAByNegotiation, LSLAData } from "$lib/data/charts/LSLAByNegotiation"
  import { filters } from "$lib/filters"
  import {
    NEGOTIATION_STATUS_GROUP_MAP,
    NegotiationStatus,
    NegotiationStatusGroup,
  } from "$lib/types/deal"
  import type { DealVersion2 } from "$lib/types/newtypes"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"

  export let deals: DealVersion2[] = []

  // Large Scale Land Acquisitions
  let title = $_("LSLA by negotiation status")
  let svgComp: SVGElement
  let svg = new LSLAByNegotiation()

  type Pots = { [key: string]: LSLAData }
  let pots: Pots = {}
  $: if (browser && deals?.length > 0) {
    const filter_negstat = $filters.negotiation_status
    const selected_neg_stat =
      filter_negstat.length > 0
        ? [...filter_negstat]
        : [
            NegotiationStatus.EXPRESSION_OF_INTEREST,
            NegotiationStatus.UNDER_NEGOTIATION,
            NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING,
            NegotiationStatus.ORAL_AGREEMENT,
            NegotiationStatus.CONTRACT_SIGNED,
            NegotiationStatus.CHANGE_OF_OWNERSHIP,
            NegotiationStatus.NEGOTIATIONS_FAILED,
            NegotiationStatus.CONTRACT_CANCELED,
            NegotiationStatus.CONTRACT_EXPIRED,
          ]
    if (selected_neg_stat.includes(NegotiationStatus.EXPRESSION_OF_INTEREST))
      pots.EXPRESSION_OF_INTEREST = new LSLAData(
        NegotiationStatus.EXPRESSION_OF_INTEREST,
      )
    if (selected_neg_stat.includes(NegotiationStatus.UNDER_NEGOTIATION))
      pots.UNDER_NEGOTIATION = new LSLAData(NegotiationStatus.UNDER_NEGOTIATION)
    if (selected_neg_stat.includes(NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING))
      pots.MEMORANDUM_OF_UNDERSTANDING = new LSLAData(
        NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING,
      )
    if (
      selected_neg_stat.includes(NegotiationStatus.EXPRESSION_OF_INTEREST) &&
      selected_neg_stat.includes(NegotiationStatus.UNDER_NEGOTIATION) &&
      selected_neg_stat.includes(NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING)
    )
      pots.INTENDED = new LSLAData(NegotiationStatusGroup.INTENDED, true)
    if (selected_neg_stat.includes(NegotiationStatus.ORAL_AGREEMENT))
      pots.ORAL_AGREEMENT = new LSLAData(NegotiationStatus.ORAL_AGREEMENT)
    if (selected_neg_stat.includes(NegotiationStatus.CONTRACT_SIGNED))
      pots.CONTRACT_SIGNED = new LSLAData(NegotiationStatus.CONTRACT_SIGNED)
    if (selected_neg_stat.includes(NegotiationStatus.CHANGE_OF_OWNERSHIP))
      pots.CHANGE_OF_OWNERSHIP = new LSLAData(NegotiationStatus.CHANGE_OF_OWNERSHIP)
    if (
      selected_neg_stat.includes(NegotiationStatus.ORAL_AGREEMENT) &&
      selected_neg_stat.includes(NegotiationStatus.CONTRACT_SIGNED) &&
      selected_neg_stat.includes(NegotiationStatus.CHANGE_OF_OWNERSHIP)
    )
      pots.CONCLUDED = new LSLAData(NegotiationStatusGroup.CONCLUDED, true)
    if (selected_neg_stat.includes(NegotiationStatus.NEGOTIATIONS_FAILED))
      pots.NEGOTIATIONS_FAILED = new LSLAData(NegotiationStatus.NEGOTIATIONS_FAILED)
    if (selected_neg_stat.includes(NegotiationStatus.CONTRACT_CANCELED))
      pots.CONTRACT_CANCELED = new LSLAData(NegotiationStatus.CONTRACT_CANCELED)
    if (
      selected_neg_stat.includes(NegotiationStatus.NEGOTIATIONS_FAILED) &&
      selected_neg_stat.includes(NegotiationStatus.CONTRACT_CANCELED)
    )
      pots.FAILED = new LSLAData(NegotiationStatusGroup.FAILED, true)
    if (selected_neg_stat.includes(NegotiationStatus.CONTRACT_EXPIRED))
      pots.CONTRACT_EXPIRED = new LSLAData(NegotiationStatus.CONTRACT_EXPIRED, true)

    deals.forEach(d => {
      if (!d.current_negotiation_status) return
      ;(pots[d.current_negotiation_status] as LSLAData).add(
        d.current_contract_size,
        d.intended_size,
      )
      const ngrp = NEGOTIATION_STATUS_GROUP_MAP[d.current_negotiation_status]
      if (ngrp && pots[ngrp])
        (pots[ngrp] as LSLAData).add(d.current_contract_size, d.intended_size)
    })

    svg.do_the_graph(svgComp, Object.values(pots))
  }

  const toCSV = (pots: Pots) => {
    const header = "Name (Status Group),Number of Deals,Contract Size,Intended Size\n"
    const records = Object.values(pots)
      .map(
        ({ name, amount, contract_size, intended_size }) =>
          `${name},${amount},${contract_size},${intended_size}`,
      )
      .join("\n")
    return header + records
  }
  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    if ($tracker) $tracker.trackEvent("Chart", "LSLA by negotiation", fileType)
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(pots, null, 2), title)
      case "csv":
        return downloadCSV(toCSV(pots), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }

  onMount(() => svg.do_the_graph(svgComp, Object.values(pots)))
</script>

<ChartWrapper {title} on:download={handleDownload}>
  <svg
    class="stroke-gray-700 stroke-[0.2]"
    id="lsla-by-negotiation-chart"
    bind:this={svgComp}
  />
  <!-- TODO: @Kurt needs text -->
  <!--  <div slot="legend" />-->
</ChartWrapper>
