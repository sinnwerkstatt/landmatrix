<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    NEGOTIATION_STATUS_GROUP_COLORS,
    negotiationStatusGroupReducer,
  } from "$lib/data/charts/negotiationStatusGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { fieldChoices, getFieldChoicesLabel } from "$lib/stores"
  import { NegotiationStatusGroup, type DealVersion2 } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: getStatusGroupLabel = getFieldChoicesLabel(
    $fieldChoices["deal"]["negotiation_status_group"],
  ) as (key: NegotiationStatusGroup) => string

  $: createData = createChartData<NegotiationStatusGroup>(
    negotiationStatusGroupReducer,
    Object.values(NegotiationStatusGroup),
    getStatusGroupLabel,
    (key: NegotiationStatusGroup) => NEGOTIATION_STATUS_GROUP_COLORS[key],
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Negotiation status")} {data} {unit} />
