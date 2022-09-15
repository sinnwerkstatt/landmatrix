<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import { classification_choices } from "$lib/choices"
  import { DynamicsOfDeal, toCSV, toJSON } from "$lib/data/charts/dynamicsOfDeal"
  import type { DynamicsDataPoint } from "$lib/data/charts/dynamicsOfDeal"
  import type { Deal } from "$lib/types/deal"

  import ChartWrapper from "$components/Data/Charts/ChartWrapper.svelte"
  import {
    downloadCSV,
    downloadImage,
    downloadJSON,
  } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"

  const title = $_("Dynamics of deal by investor type")
  const dynamicOfDeal = new DynamicsOfDeal()

  export let deals: Deal[] = []

  let svgComp: SVGElement

  let multideals = 0
  let payload: DynamicsDataPoint[] = []

  $: if (browser && deals?.length > 0) {
    let pots: { [key: string]: number } = {}
    deals.forEach(d => {
      if (d.top_investors.length > 1) multideals += 1
      d.top_investors.forEach(i => {
        const cl = i.classification
        pots[cl] = pots[cl]
          ? pots[cl] + d.current_contract_size
          : d.current_contract_size
      })
    })

    payload = Object.entries(pots).map(([k, v]) => ({
      name: $_(classification_choices[k]) || $_("Unknown"),
      value: v,
    }))

    dynamicOfDeal.do_the_graph(svgComp, payload)
  }

  const handleDownload = (event: DownloadEvent) => {
    const fileType = event.detail

    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(payload), title)
      case "csv":
        return downloadCSV(toCSV(payload), title)
      default:
        return downloadImage(svgComp, fileType, title)
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
