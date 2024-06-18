<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import { DynamicsOfDeal, toCSV, toJSON } from "$lib/data/charts/dynamicsOfDeal"
  import type { DynamicsDataPoint } from "$lib/data/charts/dynamicsOfDeal"
  import { createLabels, fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"

  $: title = $_("Dynamics of deal by investor type")
  const dynamicOfDeal = new DynamicsOfDeal()

  export let deals: DealVersion2[] = []

  let svgComp: SVGElement

  let multideals = 0
  let payload: DynamicsDataPoint[] = []

  $: classificationLabels = createLabels($fieldChoices.investor.classification)

  $: if (browser && deals?.length > 0) {
    let pots: { [key: string]: number } = {}
    deals.forEach(d => {
      if (d.top_investors.length > 1) multideals += 1
      d.top_investors.forEach(i => {
        // FIXME: There are investors with invalid classifications null or ''
        let cl = i.classification
        if (cl === "" || cl === null) cl = "unknown"

        const dealSize = d.current_contract_size ?? 0
        pots[cl] = pots[cl] ? pots[cl] + dealSize : dealSize
      })
    })

    payload = Object.entries(pots).map(([k, v]) => ({
      name: classificationLabels[k] || $_("Unknown"),
      value: v,
    }))

    dynamicOfDeal.do_the_graph(svgComp, payload)
  }

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
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

  onMount(() => dynamicOfDeal.do_the_graph(svgComp, payload))
</script>

<ChartWrapper {title} on:download={handleDownload}>
  <svg id="dynamics-of-deal-chart" bind:this={svgComp} />

  <div slot="legend">
    {$_(
      "Please note: {number} deals have multiple investor types. The full size of the deal is assigned to each investor type.",
      { values: { number: multideals } },
    )}
  </div>
</ChartWrapper>
