<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    NEGOTIATION_STATUS_GROUP_COLORS,
    negotiationStatusGroupReducer,
  } from "$lib/data/charts/negotiationStatusGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { negotiationStatusGroupMap } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import { NegotiationStatusGroup } from "$lib/types/deal"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: Deal[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: createData = createChartData<NegotiationStatusGroup>(
    negotiationStatusGroupReducer,
    Object.values(NegotiationStatusGroup),
    (key: NegotiationStatusGroup) => $negotiationStatusGroupMap[key],
    (key: NegotiationStatusGroup) => NEGOTIATION_STATUS_GROUP_COLORS[key],
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Negotiation status")} {data} {unit} />
