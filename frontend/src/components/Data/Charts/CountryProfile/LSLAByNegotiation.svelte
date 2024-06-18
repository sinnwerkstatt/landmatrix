<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import { LSLAByNegotiation, LSLAData } from "$lib/data/charts/LSLAByNegotiation"
  import { filters } from "$lib/filters"
  import { createGroupMap, createLabels, fieldChoices } from "$lib/stores"
  import {
    NegotiationStatusGroup,
    type DealVersion2,
    type NegotiationStatus,
    type NegStatGroupMap,
  } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"

  export let deals: DealVersion2[] = []

  $: negStatChoices = $fieldChoices.deal.negotiation_status
  $: negStatLabels = createLabels<NegotiationStatus>(negStatChoices)

  $: negStatGroupChoices = $fieldChoices.deal.negotiation_status_group
  $: negStatGroupLabels = createLabels<NegotiationStatusGroup>(negStatGroupChoices)

  $: negStatGroupMap = createGroupMap<NegStatGroupMap>(negStatChoices)

  // Large Scale Land Acquisitions
  $: title = $_("LSLA by negotiation status")

  let svgComp: SVGElement
  let svg = new LSLAByNegotiation()

  type Pots = {
    [key in NegotiationStatus | NegotiationStatusGroup]: LSLAData
  }
  let pots: Pots

  $: if (browser && deals?.length > 0) {
    pots = {} as Pots

    const filterNegStats = $filters.negotiation_status
    const selectedNegStats =
      filterNegStats.length > 0
        ? [...filterNegStats]
        : negStatChoices.map(x => x.value as NegotiationStatus)

    negStatGroupChoices
      .map(x => x.value as NegotiationStatusGroup)
      .forEach(negStatGroup => {
        const groupNegStats = negStatChoices
          .filter(x => x.group === negStatGroup)
          .map(x => x.value) as NegotiationStatus[]

        groupNegStats
          .filter(negStat => selectedNegStats.includes(negStat))
          .forEach(negStat => {
            pots[negStat] = new LSLAData(negStatLabels[negStat])
          })

        if (groupNegStats.every(negStat => selectedNegStats.includes(negStat))) {
          pots[negStatGroup] = new LSLAData(negStatGroupLabels[negStatGroup], true)
        }
      })

    // TODO: reduce deals
    deals.forEach(d => {
      if (
        !d.current_negotiation_status ||
        // could happen on filter update before deals update
        !selectedNegStats.includes(d.current_negotiation_status)
      )
        return

      pots[d.current_negotiation_status].add(d.current_contract_size, d.intended_size)

      const ngrp = negStatGroupMap[d.current_negotiation_status]

      if (ngrp && pots[ngrp]) pots[ngrp].add(d.current_contract_size, d.intended_size)
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
