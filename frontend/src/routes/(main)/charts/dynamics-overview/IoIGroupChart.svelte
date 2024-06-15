<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    INTENTION_OF_INVESTMENT_GROUP_COLORS,
    intentionOfInvestmentGroupReducer,
  } from "$lib/data/charts/intentionOfInvestmentGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { fieldChoices, getFieldChoicesLabel } from "$lib/stores"
  import { IntentionOfInvestmentGroup, type DealVersion2 } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: ioiGroupChoices = $fieldChoices["deal"]["intention_of_investment_group"]
  $: getIoIGroupLabel = getFieldChoicesLabel(ioiGroupChoices) as (
    group: IntentionOfInvestmentGroup,
  ) => string

  // TODO: Refactor - Why recreate the data on group label change?
  $: createData = createChartData<IntentionOfInvestmentGroup>(
    intentionOfInvestmentGroupReducer,
    Object.values(IntentionOfInvestmentGroup),
    getIoIGroupLabel,
    (key: IntentionOfInvestmentGroup) => INTENTION_OF_INVESTMENT_GROUP_COLORS[key],
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Intention of investment")} {data} {unit} />
