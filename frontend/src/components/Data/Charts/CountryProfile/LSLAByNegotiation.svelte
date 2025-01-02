<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { _ } from "svelte-i18n"

  import { LSLAByNegotiation, LSLAData } from "$lib/data/charts/LSLAByNegotiation"
  import { createGroupMap, createLabels, dealChoices } from "$lib/fieldChoices"
  import { filters } from "$lib/filters"
  import {
    NegotiationStatusGroup,
    type DealVersion2,
    type NegotiationStatus,
    type NegStatGroupMap,
  } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"

  interface Props {
    deals?: DealVersion2[]
  }

  let { deals = [] }: Props = $props()

  let negStatChoices = $derived($dealChoices.negotiation_status)
  let negStatLabels = $derived(createLabels<NegotiationStatus>(negStatChoices))

  let negStatGroupChoices = $derived($dealChoices.negotiation_status_group)
  let negStatGroupLabels = $derived(
    createLabels<NegotiationStatusGroup>(negStatGroupChoices),
  )

  let negStatGroupMap = $derived(createGroupMap<NegStatGroupMap>(negStatChoices))

  // Large Scale Land Acquisitions
  let title = $derived($_("LSLA by negotiation status"))

  let svgComp: SVGElement | undefined = $state()
  let svg = new LSLAByNegotiation()

  type Pots = {
    [key in NegotiationStatus | NegotiationStatusGroup]: LSLAData
  }
  let pots: Pots = $derived.by(() => {
    let _pots = {} as Pots

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
            _pots[negStat] = new LSLAData(negStatLabels[negStat])
          })

        if (groupNegStats.every(negStat => selectedNegStats.includes(negStat))) {
          _pots[negStatGroup] = new LSLAData(negStatGroupLabels[negStatGroup], true)
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

      _pots[d.current_negotiation_status].add(d.current_contract_size, d.intended_size)

      const ngrp = negStatGroupMap[d.current_negotiation_status]

      if (ngrp && _pots[ngrp]) _pots[ngrp].add(d.current_contract_size, d.intended_size)
    })
    return _pots
  })

  $effect(() => {
    if (svgComp && deals?.length > 0) {
      svg.do_the_graph(svgComp, Object.values(pots))
    }
  })

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
  const handleDownload = (fileType: FileType) => {
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
</script>

<ChartWrapper ondownload={handleDownload} {title}>
  <svg
    bind:this={svgComp}
    class="stroke-gray-700 stroke-[0.2]"
    id="lsla-by-negotiation-chart"
  />
  <!-- TODO: @Kurt needs text -->
  <!--  <div slot="legend" />-->
</ChartWrapper>
