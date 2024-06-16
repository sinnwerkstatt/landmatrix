<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import { createAgricultureIntentionReducer } from "$lib/data/charts/agricultureIntention"
  import type { IoIGroupMap } from "$lib/data/charts/intentionOfInvestmentGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { fieldChoices } from "$lib/stores"
  import { type DealVersion2, type IntentionOfInvestment } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"

  export let deals: DealVersion2[] = []
  export let displayDealsCount = false

  let sortBy: SortBy
  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: ioiChoices = $fieldChoices["deal"]["intention_of_investment"]
  $: ioiGroupMap = ioiChoices.reduce(
    (acc, { value, group }) => ({ ...acc, [value]: group }),
    {},
  ) as IoIGroupMap
  $: ioiLabels = ioiChoices.reduce(
    (acc, { value, label }) => ({ ...acc, [value]: label }),
    {},
  ) as { [key in IntentionOfInvestment]: string }

  $: createData = createChartData<IntentionOfInvestment>(
    createAgricultureIntentionReducer(ioiGroupMap),
    ioiChoices.map(x => x.value) as IntentionOfInvestment[],
    (ioi: IntentionOfInvestment) => ioiLabels[ioi],
    (_, index, array) => {
      const alphaValue = 1 - index / array.length
      return `rgba(252,148,31,${alphaValue})`
    },
  )

  $: data = createData(deals, sortBy)
</script>

<DownloadablePieChart title={$_("Investment in agriculture")} {data} {unit} />
