<script lang="ts">
  import * as R from "ramda"
  import type { ChartData, ChartOptions, LegendItem } from "chart.js"
  import {
    ArcElement,
    Tooltip,
    Title,
    SubTitle,
    Legend,
    Chart as ChartJS,
  } from "chart.js?client"
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import type { Deal } from "$lib/types/deal"
  import { IoI, INTENTION_OF_INVESTMENT_GROUP_MAP } from "$lib/types/deal"
  import {
    createBucketMapReducer,
    createEmptyBuckets,
    bucketEntries,
  } from "$lib/data/buckets"
  import { isConcluded } from "$lib/data/dealUtils"
  import { intention_of_investment_group_choices } from "$lib/choices"

  import DoughnutWrapper from "$components/Data/Charts/CountryProfile/DoughnutWrapper.svelte"

  import type { GroupedEntries, Item, GroupedBuckets } from "./LACP"
  import {
    getSortedEntries,
    createBackgroundColors,
    createData,
    createGroupData,
    IOI_GROUP_COLORS,
  } from "./LACP"

  ChartJS.register(ArcElement, Tooltip, Title, SubTitle, Legend)

  export let deals: Deal[] = []

  let sortBy: SortBy = "count"

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

  let groupedBuckets: GroupedBuckets
  $: groupedBuckets = bucketEntries(buckets).reduce((groups, [key, bucket]) => {
    const group = INTENTION_OF_INVESTMENT_GROUP_MAP[key]
    return {
      ...groups,
      [group]: {
        ...groups[group],
        [key]: bucket,
      },
    }
  }, {} as GroupedBuckets)

  let sortedGroupedEntries: GroupedEntries
  $: sortedGroupedEntries = getSortedEntries(sortBy, groupedBuckets)

  let data: ChartData<"doughnut", Item[]>
  $: data = {
    labels: sortedGroupedEntries.map(([key]) =>
      $_(intention_of_investment_group_choices[key]),
    ),
    datasets: [
      {
        label: $_("Category"),
        data: createData(_, sortBy)(sortedGroupedEntries),
        backgroundColor: createBackgroundColors(sortedGroupedEntries),
        normalized: true,
        borderWidth: 1,
        // weight: 3,
      },
      {
        label: $_("Group"),
        data: createGroupData(_, sortBy)(sortedGroupedEntries),
        backgroundColor: sortedGroupedEntries.map(([key]) => IOI_GROUP_COLORS[key]),
        normalized: true,
        // weight: 2,
        borderWidth: 2,
      },
    ],
  }

  let options: ChartOptions<"doughnut">
  $: options = {
    // aspectRatio: 1.2,
    maintainAspectRatio: false,
    cutout: "30%",
    plugins: {
      tooltip: {
        callbacks: {
          label(context) {
            const item = context.raw as Item
            const percentage = item["value"] * 100
            return ` ${percentage.toFixed(2)}%`
          },
          title(items) {
            return (items[0].raw as Item)["label"]
          },
        },
      },
      title: {
        display: true,
        text: $_("Land acquisitions by category of production"),
        font: {
          size: 35,
        },
      },
      subtitle: {
        display: true,
        position: "bottom",
        text: [
          (sortBy === "count" ? "Number of deals" : "Size under contract") +
            " per category of production,",
          "represented as the percentage of total",
          sortBy === "count" ? "concluded deals" : "concluded size",
        ],
        font: {
          size: 25,
        },
      },
      legend: {
        display: true,
        labels: {
          font: {
            size: 20,
          },
          generateLabels(chart: ChartJS) {
            const original =
              ChartJS.overrides.doughnut.plugins.legend.labels.generateLabels
            const labelsOriginal: LegendItem[] = original.call(this, chart)

            const groupColors = chart.data.datasets[1].backgroundColor

            return labelsOriginal.map((label, index) => ({
              ...label,
              fillStyle: groupColors[index],
            }))
          },
        },
        onClick(event, legendItem, legend) {
          const groupIndex = legendItem.index as number
          const chart = legend.chart

          const hiddenGroups =
            legend.legendItems?.map((item, index) =>
              groupIndex === index ? !item.hidden : item.hidden,
            ) ?? []

          const booleanMask = sortedGroupedEntries
            .map(([_, entries], i) => {
              return R.repeat(groupIndex == i, entries.length)
            })
            .flat()

          if (hiddenGroups[groupIndex]) {
            chart.hide(1, groupIndex)
            booleanMask.forEach((val, index) => {
              if (val) {
                chart.hide(0, index)
              }
            })
          } else {
            chart.show(1, groupIndex)
            booleanMask.forEach((val, index) => {
              if (val) {
                chart.show(0, index)
              }
            })
          }
          legend.legendItems?.forEach((item, index) => {
            item.hidden = hiddenGroups[index]
          })
        },
      },
    },
  }
</script>

<!-- https://www.chartjs.org/docs/latest/configuration/responsive.html#important-note-->
<div class="relative mx-auto h-[80vh] p-5 md:p-10">
  <DoughnutWrapper {data} {options} />
</div>

<button
  class="btn btn-primary"
  on:click={() => {
    sortBy = sortBy === "count" ? "size" : "count"
  }}
>
  {$_("Show deal")}
  {sortBy === "count" ? "size" : "count"}
</button>
