<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import type { DynamicsDataPoint } from "$lib/data/charts/dynamicsOfDeal"
  import { DynamicsOfDeal, toCSV, toJSON } from "$lib/data/charts/dynamicsOfDeal"
  import { createLabels, fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"

  let title = $derived($_("Dynamics of deal by investor type"))
  const dynamicOfDeal = new DynamicsOfDeal()

  interface Props {
    deals?: DealVersion2[]
  }

  let { deals = [] }: Props = $props()

  let svgComp: SVGElement | undefined = $state()

  let multideals = $derived(deals.filter(d => d.top_investors.length > 1).length)

  let classificationLabels = $derived(
    createLabels($fieldChoices.investor.classification),
  )
  const payload: DynamicsDataPoint[] = $derived.by(() => {
    let pots: { [key: string]: number } = {}
    deals.forEach(d => {
      d.top_investors.forEach(i => {
        // FIXME: There are investors with invalid classifications null or ''
        let cl = i.classification
        if (cl === "" || cl === null) cl = "unknown"

        const dealSize = d.current_contract_size ?? 0
        pots[cl] = pots[cl] ? pots[cl] + dealSize : dealSize
      })
    })

    return Object.entries(pots).map(([k, v]) => ({
      name: classificationLabels[k] || $_("Unknown"),
      value: v,
    }))
  })

  $effect(() => {
    if (browser && svgComp && deals?.length > 0) {
      dynamicOfDeal.do_the_graph(svgComp, payload)
    }
  })

  const handleDownload = (fileType: FileType) => {
    if ($tracker) $tracker.trackEvent("Chart", "Dynamics of deal", fileType)
    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(payload), title)
      case "csv":
        return downloadCSV(toCSV(payload), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }
</script>

<ChartWrapper ondownload={handleDownload} {title}>
  <svg bind:this={svgComp} id="dynamics-of-deal-chart" />

  {#snippet legend()}
    <div>
      {$_(
        "Please note: {number} deals have multiple investor types. The full size of the deal is assigned to each investor type.",
        { values: { number: multideals } },
      )}
    </div>
  {/snippet}
</ChartWrapper>
