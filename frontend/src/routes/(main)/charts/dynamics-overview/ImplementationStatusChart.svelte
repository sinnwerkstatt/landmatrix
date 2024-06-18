<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    IMPLEMENTATION_STATUS_COLORS,
    implementationStatusReducer,
  } from "$lib/data/charts/implementationStatus"
  import { createChartData } from "$lib/data/createChartData"
  import { createLabels, fieldChoices } from "$lib/stores"
  import type { DealVersion2, ImplementationStatus } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: impStatChoices = $fieldChoices.deal.implementation_status
  $: impStatLabels = createLabels<ImplementationStatus>(impStatChoices)

  $: createData = createChartData<ImplementationStatus>(
    implementationStatusReducer,
    impStatChoices.map(x => x.value) as ImplementationStatus[],
    (key: ImplementationStatus) => impStatLabels[key],
    (key: ImplementationStatus) => IMPLEMENTATION_STATUS_COLORS[key],
  )

  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Implementation status")} {data} {unit} />
