<script lang="ts">
  import { _, number } from "svelte-i18n"
  import * as R from "ramda"

  import type { Deal } from "$lib/types/deal"
  import {
    createChartData,
    clearGraph,
    drawGraph,
  } from "$lib/data/charts/concludedDealsOverTime"
  import type { ChartData } from "$lib/data/charts/concludedDealsOverTime"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"

  export let deals: Deal[] = []
  export const START_YEAR = 2000

  $: title = $_("Concluded deals over time since the year {year}", {
    values: { year: START_YEAR },
  })

  let svgComp: SVGElement

  let chartData: ChartData
  $: chartData = createChartData(START_YEAR, deals)

  $: if (svgComp) {
    clearGraph(svgComp)
    drawGraph(svgComp, chartData.counts)
  }

  export const toJSON: (data: [Date, number][]) => string = R.pipe(
    R.map(([date, count]) => ({ year: date.getFullYear(), count })),
    R.partialRight(JSON.stringify, [null, 2]),
  )

  export const toCSV: (data: [Date, number][]) => string = R.pipe(
    R.map(([date, count]) => `${date.getFullYear()},${count}`),
    R.prepend("Year,Count"),
    R.join("\n"),
  )

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(chartData.counts), title)
      case "csv":
        return downloadCSV(toCSV(chartData.counts), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }
</script>

<ChartWrapper {title} on:download={handleDownload}>
  <svg fill="#cce5df" stroke="#69b3a2" bind:this={svgComp} />

  <div slot="legend">
    {$_(
      "Note: There is no year information for {count} deals with a corresponding area size of {size} ha.",
      {
        values: {
          count: $number(chartData.excluded.count),
          size: $number(chartData.excluded.size),
        },
      },
    )}
  </div>
</ChartWrapper>
