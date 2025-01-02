<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    IMPLEMENTATION_STATUS_COLORS,
    implementationStatusReducer,
  } from "$lib/data/charts/implementationStatus"
  import { createChartData } from "$lib/data/createChartData"
  import { createLabels, dealChoices } from "$lib/fieldChoices"
  import type { DealVersion2, ImplementationStatus } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  interface Props {
    deals?: DealVersion2[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  let sortBy: SortBy = $derived(displayDealsCount ? "count" : "size")

  let unit = $derived(displayDealsCount ? "deals" : "ha")

  let impStatChoices = $derived($dealChoices.implementation_status)
  let impStatLabels = $derived(createLabels<ImplementationStatus>(impStatChoices))

  let createData = $derived(
    createChartData<ImplementationStatus>(
      implementationStatusReducer,
      impStatChoices.map(x => x.value) as ImplementationStatus[],
      (key: ImplementationStatus) => impStatLabels[key],
      (key: ImplementationStatus) => IMPLEMENTATION_STATUS_COLORS[key],
    ),
  )

  let data = $derived(createData(deals, sortBy))
</script>

<DownloadablePieChart {data} title={$_("Implementation status")} {unit} />
