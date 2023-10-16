<script lang="ts">
  import { _ } from "svelte-i18n"
  import * as R from "ramda"

  import type { Deal, IoIGroup } from "$lib/types/deal"
  import type { SortBy } from "$lib/data/buckets"
  import { isConcluded } from "$lib/data/dealUtils"
  import {
    createBucketMapReducer,
    createEmptyBuckets,
    bucketEntries,
  } from "$lib/data/buckets"
  import { IoI, INTENTION_OF_INVESTMENT_GROUP_MAP } from "$lib/types/deal"
  import { intentionOfInvestmentMap, intentionOfInvestmentGroupMap } from "$lib/stores"
  import { clearGraph } from "$lib/data/charts/concludedDealsOverTime"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    drawGraph,
    IOI_GROUP_COLORS,
  } from "$components/Data/Charts/CountryProfile/LACP"
  import type { Data } from "$components/Data/Charts/CountryProfile/LACP"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { downloadJSON, downloadCSV, downloadSVG } from "$components/Data/Charts/utils"
  import { displayDealsCount } from "$components/Map/map_helper.js"

  export let deals: Deal[] = []

  let sortBy: SortBy
  $: sortBy = $displayDealsCount ? "count" : "size"

  $: filtered = deals.filter(isConcluded)

  $: buckets = filtered.reduce((buckets, deal) => {
    const intentions = deal.current_intention_of_investment ?? []
    return intentions.reduce(
      createBucketMapReducer(
        (deal.deal_size ?? 0) / intentions.length,
        1 / intentions.length,
      ),
      buckets,
    )
  }, createEmptyBuckets(Object.values(IoI)))

  let data: Data
  $: data = bucketEntries(buckets)
    .map(([key, value]) => {
      const groupKey = INTENTION_OF_INVESTMENT_GROUP_MAP[key]
      return {
        key,
        label: $intentionOfInvestmentMap[key],
        value: sortBy === "count" ? value.count : value.size,
        groupKey,
        groupLabel: $intentionOfInvestmentGroupMap[groupKey],
        color: IOI_GROUP_COLORS[groupKey],
      }
    })
    .sort((a, b) => b.value - a.value)

  let svgElement: SVGElement

  $: title = $_("Land acquisitions by category of production")
  $: xLabel = $_("Category of production")
  $: yLabel = $displayDealsCount ? $_("Number of deals") : $_("Deal size (ha)")
  $: groups = Object.entries<string>($intentionOfInvestmentGroupMap).map(entry => {
    const key = entry[0] as IoIGroup
    return {
      key,
      label: entry[1],
      color: IOI_GROUP_COLORS[key],
    }
  })

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
    class="stroke-lm-dark stroke-[0.2] font-oswald text-lm-dark dark:text-white"
  />
</ChartWrapper>
