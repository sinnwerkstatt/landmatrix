<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import * as R from "ramda"
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    bucketEntries,
    createBucketMapReducer,
    createEmptyBuckets,
  } from "$lib/data/buckets"
  import { clearGraph } from "$lib/data/charts/concludedDealsOverTime"
  import { isConcluded } from "$lib/data/dealUtils"
  import { createGroupMap, createLabels, fieldChoices } from "$lib/stores"
  import {
    IntentionOfInvestmentGroup,
    type DealVersion2,
    type IntentionOfInvestment,
    type IoIGroupMap,
  } from "$lib/types/data"

  import {
    drawGraph,
    IOI_GROUP_COLORS,
  } from "$components/Data/Charts/CountryProfile/LACP"
  import type { Data } from "$components/Data/Charts/CountryProfile/LACP"
  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import { displayDealsCount } from "$components/Map/mapHelper"

  export let deals: DealVersion2[] = []

  let sortBy: SortBy
  $: sortBy = $displayDealsCount ? "count" : "size"
  $: legendText =
    sortBy === "count"
      ? $_(
          "Number of deals per category of production as a percentage of all concluded deals",
        )
      : $_(
          "Size under contract per category of production as a percentage of total size of all concluded deals",
        )

  $: filtered = deals.filter(isConcluded)

  $: buckets = filtered.reduce(
    (buckets, deal) => {
      const intentions = deal.current_intention_of_investment ?? []
      return intentions.reduce(
        createBucketMapReducer(
          (deal.deal_size ?? 0) / intentions.length,
          1 / intentions.length,
        ),
        buckets,
      )
    },
    createEmptyBuckets(ioiChoices.map(x => x.value) as IntentionOfInvestment[]),
  )

  $: ioiChoices = $fieldChoices.deal.intention_of_investment
  $: ioiLabels = createLabels<IntentionOfInvestment>(ioiChoices)

  $: ioiGroups = $fieldChoices.deal.intention_of_investment_group
  $: ioiGroupLabels = createLabels<IntentionOfInvestmentGroup>(ioiGroups)

  $: ioiGroupMap = createGroupMap<IoIGroupMap>(ioiChoices)

  let data: Data
  $: data = bucketEntries(buckets)
    .map(([key, value]) => {
      const groupKey = ioiGroupMap[key]
      return {
        key,
        label: ioiLabels[key],
        value: sortBy === "count" ? value.count : value.size,
        groupKey,
        groupLabel: ioiGroupLabels[groupKey],
        color: IOI_GROUP_COLORS[groupKey],
      }
    })
    .sort((a, b) => b.value - a.value)

  let svgElement: SVGElement

  $: title = $_("Land acquisitions by category of production")
  $: xLabel = $_("Category of production")
  $: yLabel = $displayDealsCount ? $_("Deals / Total Deals") : $_("Size / Total Size")

  // Using groups: Maybe this is a good solution for the future
  $: groups = ioiGroups.map(entry => ({
    key: entry.value,
    label: entry.label,
    color: IOI_GROUP_COLORS[entry.value as IntentionOfInvestmentGroup],
  }))

  $: if (svgElement) {
    clearGraph(svgElement)
    drawGraph(svgElement, data, groups, title, xLabel, yLabel)
  }

  export const toJSON: (data: Data) => string = R.partialRight(JSON.stringify, [
    null,
    2,
  ])

  export const toCSV: (data: Data) => string = R.pipe(
    R.map(({ label, value }) => `${label},${value}`),
    R.prepend("Intention of investment,value"),
    R.join("\n"),
  )

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    if ($tracker)
      $tracker.trackEvent("Chart", "Land acquisitions by category", fileType)
    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(data), title)
      case "csv":
        return downloadCSV(toCSV(data), title)
      default:
        return downloadSVG(svgElement, fileType, title)
    }
  }
</script>

<ChartWrapper title="" on:download={handleDownload}>
  <svg
    bind:this={svgElement}
    class="stroke-gray-700 stroke-[0.2] text-gray-700 dark:text-white"
  />
  <div slot="legend">
    {legendText}
  </div>
</ChartWrapper>

<style lang="postcss">
  :global(.lacp-chart-legend-background) {
    @apply fill-white dark:fill-gray-900;
  }
</style>
