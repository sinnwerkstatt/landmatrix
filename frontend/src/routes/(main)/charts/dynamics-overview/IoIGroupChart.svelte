<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    INTENTION_OF_INVESTMENT_GROUP_COLORS,
    intentionOfInvestmentGroupReducer,
  } from "$lib/data/charts/intentionOfInvestmentGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { intentionOfInvestmentGroupMap } from "$lib/stores/maps"
  import type { Deal } from "$lib/types/deal"
  import { IntentionOfInvestmentGroup } from "$lib/types/deal"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: Deal[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: createData = createChartData<IntentionOfInvestmentGroup>(
    intentionOfInvestmentGroupReducer,
    Object.values(IntentionOfInvestmentGroup),
    (key: IntentionOfInvestmentGroup) => $intentionOfInvestmentGroupMap[key],
    (key: IntentionOfInvestmentGroup) => INTENTION_OF_INVESTMENT_GROUP_COLORS[key],
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Intention of investment")} {data} {unit} />
