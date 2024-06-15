<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import { agricultureIntentionReducer } from "$lib/data/charts/agricultureIntention"
  import { createChartData } from "$lib/data/createChartData"
  import { fieldChoices, getFieldChoicesLabel } from "$lib/stores"
  import type { DealVersion2, IntentionOfInvestment } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: ioiChoices = $fieldChoices["deal"]["intention_of_investment"]

  $: createData = createChartData<IntentionOfInvestment>(
    agricultureIntentionReducer,
    ioiChoices.map(x => x.value) as IntentionOfInvestment[],
    getFieldChoicesLabel(ioiChoices) as (key: IntentionOfInvestment) => string,
    (_, index, array) => {
      const alphaValue = 1 - index / array.length
      return `rgba(252,148,31,${alphaValue})`
    },
  )

  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Investment in agriculture")} {data} {unit} />
