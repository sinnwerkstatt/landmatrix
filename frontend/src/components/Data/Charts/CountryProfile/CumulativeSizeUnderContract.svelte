<script lang="ts">
  import { _ } from "svelte-i18n"
  import * as R from "ramda"

  import type { Deal } from "$lib/types/deal"
  import {
    createChartData,
    clearGraph,
    drawGraph,
  } from "$lib/data/charts/concludedDealsOverTime"
  import type { ChartData } from "$lib/data/charts/concludedDealsOverTime"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { downloadJSON, downloadCSV, downloadSVG } from "$components/Data/Charts/utils"

  export let deals: Deal[] = []

  $: title = $_("Cumulative area size under contract since the year 2000")

  let svgComp: SVGElement

  let chartData: ChartData

  $: chartData = createChartData(deals)

  $: if (svgComp) {
    clearGraph(svgComp)
    drawGraph(svgComp, chartData.sizes)
  }

  export const toJSON: (data: [Date, number][]) => string = R.pipe(
    R.map(([date, count]) => ({ year: date.getFullYear(), count })),
    R.partialRight(JSON.stringify, [null, 2]),
  )

  export const toCSV: (data: [Date, number][]) => string = R.pipe(
    R.map(([date, count]) => `${date.getFullYear()},${count}`),
    R.prepend("Year,Size(ha)"),
    R.join("\n"),
  )

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(chartData.sizes), title)
      case "csv":
        return downloadCSV(toCSV(chartData.sizes), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }
</script>

<ChartWrapper {title} on:download={handleDownload}>
  <svg fill="#fee1c0" stroke="#fc941f" bind:this={svgComp} />

  <div slot="legend">
    {$_(
      "Note: This graph shows changes in size under contract (increases/decreases). Therefore, the number of deals can remain the same even though the size may change.",
    )}
  </div>
</ChartWrapper>
