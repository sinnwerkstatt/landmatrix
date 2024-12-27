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

  interface Props {
    deals?: DealVersion2[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  let sortBy: SortBy = $derived(displayDealsCount ? "count" : "size")

  let unit = $derived(displayDealsCount ? "deals" : "ha")

  let negStatGroupMap = $derived(
    createGroupMap<NegStatGroupMap>($fieldChoices.deal.negotiation_status),
  )
  let negStatGroupLabels = $derived(
    createLabels<NegotiationStatusGroup>($fieldChoices.deal.negotiation_status_group),
  )

  let createData = $derived(
    createChartData<NegotiationStatusGroup>(
      createNegotiationStatusGroupReducer(negStatGroupMap),
      Object.values(NegotiationStatusGroup),
      (key: NegotiationStatusGroup) => negStatGroupLabels[key],
      (key: NegotiationStatusGroup) => NEGOTIATION_STATUS_GROUP_COLORS[key],
    ),
  )
  let data = $derived(createData(deals, sortBy))
</script>

<DownloadablePieChart title={$_("Negotiation status")} {data} {unit} />
