<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Deal } from "$lib/types/deal"
  import {
    IMPLEMENTATION_STATUS_COLORS,
    implementationStatusReducer,
  } from "$lib/data/charts/implementationStatus"
  import { createChartData } from "$lib/data/createChartData"
  import { ImplementationStatus } from "$lib/types/deal"
  import { implementationStatusMap } from "$lib/stores"
  import type { SortBy } from "$lib/data/buckets"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: Deal[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: createData = createChartData<ImplementationStatus>(
    implementationStatusReducer,
    Object.values(ImplementationStatus),
    (key: ImplementationStatus) => $implementationStatusMap[key],
    (key: ImplementationStatus) => IMPLEMENTATION_STATUS_COLORS[key],
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Implementation status")} {data} {unit} />
