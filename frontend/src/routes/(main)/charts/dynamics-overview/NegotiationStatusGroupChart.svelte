<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    createNegotiationStatusGroupReducer,
    NEGOTIATION_STATUS_GROUP_COLORS,
  } from "$lib/data/charts/negotiationStatusGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { createGroupMap, createLabels, fieldChoices } from "$lib/stores"
  import {
    NegotiationStatusGroup,
    type DealVersion2,
    type NegStatGroupMap,
  } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: negStatGroupMap = createGroupMap<NegStatGroupMap>(
    $fieldChoices.deal.negotiation_status,
  )
  $: negStatGroupLabels = createLabels<NegotiationStatusGroup>(
    $fieldChoices.deal.negotiation_status_group,
  )

  $: createData = createChartData<NegotiationStatusGroup>(
    createNegotiationStatusGroupReducer(negStatGroupMap),
    Object.values(NegotiationStatusGroup),
    (key: NegotiationStatusGroup) => negStatGroupLabels[key],
    (key: NegotiationStatusGroup) => NEGOTIATION_STATUS_GROUP_COLORS[key],
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Negotiation status")} {data} {unit} />
