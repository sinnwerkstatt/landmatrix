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

  interface Props {
    deals?: DealVersion2[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  let sortBy: SortBy = $derived(displayDealsCount ? "count" : "size")

  let unit = $derived(displayDealsCount ? "deals" : "ha")

  let ioiGroupMap = $derived(
    createGroupMap<IoIGroupMap>($fieldChoices.deal.intention_of_investment),
  )

  let ioiGroupLabels = $derived(
    createLabels<IntentionOfInvestmentGroup>(
      $fieldChoices.deal.intention_of_investment_group,
    ),
  )

  // TODO: Refactor - Why recreate the data on group label change?
  let createData = $derived(
    createChartData<IntentionOfInvestmentGroup>(
      createIoIGroupReducer(ioiGroupMap),
      Object.keys(ioiGroupLabels) as IntentionOfInvestmentGroup[],
      (group: IntentionOfInvestmentGroup) => ioiGroupLabels[group],
      (key: IntentionOfInvestmentGroup) => INTENTION_OF_INVESTMENT_GROUP_COLORS[key],
    ),
  )

  let data = $derived(createData(deals, sortBy))
</script>

<DownloadablePieChart title={$_("Intention of investment")} {data} {unit} />
