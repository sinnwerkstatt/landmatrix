<script lang="ts">
  import * as R from "ramda"
  import type { ChartData, ChartOptions } from "chart.js"
  import { Doughnut } from "svelte-chartjs?client"
  import { ArcElement, Tooltip, Chart as ChartJS } from "chart.js?client"

  import type { Bucket, BucketMap, SortBy } from "$lib/data/buckets"
  import type { Deal } from "$lib/types/deal"
  import { IoI, INTENTION_OF_INVESTMENT_GROUP_MAP, IoIGroup } from "$lib/types/deal"
  import {
    createBucketMapReducer,
    createEmptyBuckets,
    bucketEntries,
    sumBuckets,
  } from "$lib/data/buckets"
  import { isConcluded } from "$lib/data/dealUtils"
  import {
    flat_intention_of_investment_map,
    intention_of_investment_group_choices,
  } from "$lib/choices"

  ChartJS.register(ArcElement, Tooltip)

  export let deals: Deal[] = []
  export let displayDealsCount = true

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"

  const IOI_GROUP_COLORS: {
    [key in IoIGroup]: string
  } = {
    [IoIGroup.FORESTRY]: "#179961",
    [IoIGroup.AGRICULTURE]: "#00bfff",
    [IoIGroup.OTHER]: "#ff7c63",
  }

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

  type GroupedBuckets = { [key in IoIGroup]: BucketMap<IoI> }
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

  type GroupedEntries = [IoIGroup, [IoI, Bucket][]][]
  let sortedGroupedEntries: GroupedEntries
  $: sortedGroupedEntries = Object.entries<BucketMap>(groupedBuckets)
    .sort(
      (entry1, entry2) => sumBuckets(entry2[1])[sortBy] - sumBuckets(entry1[1])[sortBy],
    )
    .map(([key, value]) => [
      key,
      Object.entries(value).sort(
        (entry1, entry2) => entry2[1][sortBy] - entry1[1][sortBy],
      ),
    ])

  interface Item<Key extends string = string> {
    key: Key
    value: number
    label: string
  }
  let createData: (sortedEntries: GroupedEntries) => Item<IoI>[]
  $: createData = R.pipe(
    R.map(R.nth(1)),
    R.unnest,
    R.map<[IoI, Bucket], Item<IoI>>(
      ([key, bucket]) =>
        ({
          key,
          value: bucket[sortBy],
          label: flat_intention_of_investment_map[key],
        } as Item<IoI>),
    ),
    normalize,
  )

  let createGroupData: (sortedEntries: GroupedEntries) => Item<IoIGroup>[]
  $: createGroupData = R.pipe(
    R.map(([key, value]) => {
      return {
        key,
        value: R.pipe(R.map(R.nth(1)), sumBuckets, R.prop(sortBy))(value),
        label: intention_of_investment_group_choices[key],
      } as Item<IoIGroup>
    }),
    normalize,
  )

  const normalize = (items: Item[]) => {
    const total = R.pipe<[Item[]], number[], number>(
      R.map(R.prop("value")),
      R.sum,
    )(items)
    return items.map(item => ({
      ...item,
      value: item["value"] / total,
    }))
  }

  const createBackgroundColors: (entries: GroupedEntries) => string[] = R.pipe(
    R.map(([key, value]) => {
      const color = IOI_GROUP_COLORS[key]
      const count = Object.values(value).length
      return R.range(0, count).map(
        i => color + (((count - i) / (count + 1)) * 100).toFixed(0),
      )
    }),
    R.unnest,
  )

  let data: ChartData<"doughnut", Item[]>
  $: data = {
    datasets: [
      {
        label: "Intention of Investment Categories",
        data: createData(sortedGroupedEntries),
        backgroundColor: createBackgroundColors(sortedGroupedEntries),
        // weight: 3,
      },
      {
        label: "Intention of Investment Groups",
        data: createGroupData(sortedGroupedEntries),
        backgroundColor: sortedGroupedEntries.map(([key]) => IOI_GROUP_COLORS[key]),
        // weight: 2,
      },
    ],
  }

  let options: ChartOptions<"doughnut">
  $: options = {
    responsive: true,
    aspectRatio: 1,
    cutout: "30%",
    plugins: {
      tooltip: {
        callbacks: {
          label: context => {
            const item = context.raw as Item
            const percentage = item["value"] * 100
            return ` ${item["label"]} (${percentage.toFixed(2)}%) `
          },
          title() {
            return "Intention of Investment"
          },
        },
      },
    },
  }
</script>

<h2>Land Acquisition by Category of Production</h2>
<p>(Intention of Investment)</p>
<p>Showing deal {sortBy}</p>
<button
  on:click={() => {
    sortBy = sortBy === "count" ? "size" : "count"
  }}
>
  Toggle sort
</button>
<Doughnut {data} {options} />
