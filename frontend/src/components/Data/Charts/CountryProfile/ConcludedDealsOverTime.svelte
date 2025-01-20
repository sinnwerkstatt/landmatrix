<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import * as R from "ramda"
  import { _, number } from "svelte-i18n"

  import type { ChartData } from "$lib/data/charts/concludedDealsOverTime"
  import {
    clearGraph,
    createChartData,
    drawGraph,
  } from "$lib/data/charts/concludedDealsOverTime"
  import type { DealVersion2 } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"
  import { displayDealsCount } from "$components/Map/mapHelper"

  interface Props {
    deals?: DealVersion2[]
  }

  let { deals = [] }: Props = $props()
  export const START_YEAR = 2000

  let title = $derived(
    $displayDealsCount
      ? $_("Concluded deals over time since the year {year}", {
          values: { year: START_YEAR },
        })
      : $_("Cumulative area size under contract since the year {year}", {
          values: { year: START_YEAR },
        }),
  )

  let svgComp: SVGElement | undefined = $state()
  let chartData: ChartData = $derived(createChartData(START_YEAR, deals))

  $effect(() => {
    if (svgComp) {
      clearGraph(svgComp)
      drawGraph(svgComp, $displayDealsCount ? chartData.counts : chartData.sizes)
    }
  })

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

  const handleDownload = (fileType: FileType, displayDealsCount: boolean) => {
    if ($tracker) $tracker.trackEvent("Chart", "Concluded deals over time", fileType)
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

<ChartWrapper ondownload={e => handleDownload(e, $displayDealsCount)} {title}>
  <svg
    bind:this={svgComp}
    color="black"
    fill={$displayDealsCount ? "#cce5df" : "#fee1c0"}
    stroke={$displayDealsCount ? "#69b3a2" : "#fc941f"}
  />

  {#snippet legend()}
    <div>
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
  {/snippet}
</ChartWrapper>
