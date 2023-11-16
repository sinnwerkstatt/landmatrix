<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import { agricultureIntentionReducer } from "$lib/data/charts/agricultureIntention"
  import { createChartData } from "$lib/data/createChartData"
  import { intentionOfInvestmentMap } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import { AgricultureIoI } from "$lib/types/deal"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: Deal[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: createData = createChartData<AgricultureIoI>(
    agricultureIntentionReducer,
    Object.values(AgricultureIoI),
    (key: AgricultureIoI) => $intentionOfInvestmentMap[key],
    (_, index, array) => {
      const alphaValue = 1 - index / array.length
      return `rgba(252,148,31,${alphaValue})`
    },
  )
  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Investment in agriculture")} {data} {unit} />
