<script lang="ts">
  import * as R from "ramda"
  import { _, number } from "svelte-i18n"

  import {
    clearGraph,
    createChartData,
    drawGraph,
  } from "$lib/data/charts/concludedDealsOverTime"
  import type { ChartData } from "$lib/data/charts/concludedDealsOverTime"
  import type { Deal } from "$lib/types/deal"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { displayDealsCount } from "$components/Map/map_helper.js"

  export let deals: Deal[] = []
  export const START_YEAR = 2000

  $: title = $displayDealsCount
    ? $_("Concluded deals over time since the year {year}", {
        values: { year: START_YEAR },
      })
    : $_("Cumulative area size under contract since the year {year}", {
        values: { year: START_YEAR },
      })

  let svgComp: SVGElement

  let chartData: ChartData
  $: chartData = createChartData(START_YEAR, deals)

  $: if (svgComp) {
    clearGraph(svgComp)
    drawGraph(svgComp, $displayDealsCount ? chartData.counts : chartData.sizes)
  }

  export const toJSON: (displayDealsCount: boolean) => (data: ChartData) => string = (
    displayDealsCount: boolean,
  ) =>
    R.pipe(
      R.prop(displayDealsCount ? "counts" : "sizes"),
      R.map(([date, val]) => ({
        year: date.getFullYear(),
        [displayDealsCount ? "count" : "size"]: val,
      })),
      R.partialRight(JSON.stringify, [null, 2]),
    )

  export const toCSV: (displayDealsCount: boolean) => (data: ChartData) => string = (
    displayDealsCount: boolean,
  ) =>
    R.pipe(
      R.prop(displayDealsCount ? "counts" : "sizes"),
      R.map(([date, val]) => `${date.getFullYear()},${val}`),
      R.prepend(`Year,${displayDealsCount ? "Count" : "Size (Ha)"}`),
      R.join("\n"),
    )

  const handleDownload = (
    { detail: fileType }: DownloadEvent,
    displayDealsCount: boolean,
  ) => {
    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(displayDealsCount)(chartData), title)
      case "csv":
        return downloadCSV(toCSV(displayDealsCount)(chartData), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }
</script>

<ChartWrapper {title} on:download={e => handleDownload(e, $displayDealsCount)}>
  <svg
    fill={$displayDealsCount ? "#cce5df" : "#fee1c0"}
    stroke={$displayDealsCount ? "#69b3a2" : "#fc941f"}
    color="black"
    bind:this={svgComp}
  />

  <div slot="legend">
    {$displayDealsCount
      ? $_(
          "Note: There is no year information for {count} deals with a corresponding area size of {size} ha.",
          {
            values: {
              count: $number(chartData.excluded.count),
              size: $number(chartData.excluded.size),
            },
          },
        )
      : $_(
          "Note: This graph shows changes in size under contract (increases/decreases). Therefore, the number of deals can remain the same even though the size may change.",
        )}
  </div>
</ChartWrapper>
