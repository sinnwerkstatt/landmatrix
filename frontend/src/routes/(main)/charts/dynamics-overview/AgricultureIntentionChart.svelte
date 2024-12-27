<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import { createAgricultureIntentionReducer } from "$lib/data/charts/agricultureIntention"
  import { createChartData } from "$lib/data/createChartData"
  import { createGroupMap, createLabels, fieldChoices } from "$lib/stores"
  import {
    type DealVersion2,
    type IntentionOfInvestment,
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

  let ioiChoices = $derived($fieldChoices.deal.intention_of_investment)
  let ioiGroupMap = $derived(createGroupMap<IoIGroupMap>(ioiChoices))
  let ioiLabels = $derived(createLabels<IntentionOfInvestment>(ioiChoices))

  let createData = $derived(
    createChartData<IntentionOfInvestment>(
      createAgricultureIntentionReducer(ioiGroupMap),
      ioiChoices.map(x => x.value) as IntentionOfInvestment[],
      (ioi: IntentionOfInvestment) => ioiLabels[ioi],
      (_, index, array) => {
        const alphaValue = 1 - index / array.length
        return `rgba(252,148,31,${alphaValue})`
      },
    ),
  )

  let data = $derived(createData(deals, sortBy))
</script>

<DownloadablePieChart title={$_("Investment in agriculture")} {data} {unit} />
