<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import {
    createIoIGroupReducer,
    INTENTION_OF_INVESTMENT_GROUP_COLORS,
  } from "$lib/data/charts/intentionOfInvestmentGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { createGroupMap, createLabels, fieldChoices } from "$lib/stores"
  import {
    IntentionOfInvestmentGroup,
    type DealVersion2,
    type IoIGroupMap,
  } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: ioiGroupMap = createGroupMap<IoIGroupMap>(
    $fieldChoices.deal.intention_of_investment,
  )

  $: ioiGroupLabels = createLabels<IntentionOfInvestmentGroup>(
    $fieldChoices.deal.intention_of_investment_group,
  )

  // TODO: Refactor - Why recreate the data on group label change?
  $: createData = createChartData<IntentionOfInvestmentGroup>(
    createIoIGroupReducer(ioiGroupMap),
    Object.keys(ioiGroupLabels) as IntentionOfInvestmentGroup[],
    (group: IntentionOfInvestmentGroup) => ioiGroupLabels[group],
    (key: IntentionOfInvestmentGroup) => INTENTION_OF_INVESTMENT_GROUP_COLORS[key],
  )

  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Intention of investment")} {data} {unit} />
