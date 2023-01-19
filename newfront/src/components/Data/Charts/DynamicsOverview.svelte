<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createAgricultureIntentionChartData } from "$lib/data/charts/agricultureIntention"
  import { createImplementationStatusChartData } from "$lib/data/charts/implementationStatus"
  import { createIntentionOfInvestmentGroupChartData } from "$lib/data/charts/intentionOfInvestmentGroup"
  import { createNegotiationStatusChartData } from "$lib/data/charts/negotiationStatusGroup"
  import type { Deal } from "$lib/types/deal"

  import DownloadablePieChart from "./DownloadablePieChart.svelte"

  export let deals: Deal[] = []
  export let displayDealsCount = false

  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: chartImpStat = createImplementationStatusChartData(deals, sortBy)
  $: chartNegStat = createNegotiationStatusChartData(deals, sortBy)
  $: chartIoI = createIntentionOfInvestmentGroupChartData(deals, sortBy)
  $: chartIoIAgriculture = createAgricultureIntentionChartData(deals, sortBy)
</script>

<div>
  <div class="grid grid-cols-2 grid-rows-2 gap-4">
    <DownloadablePieChart
      title={$_("Intention of investment")}
      data={chartIoI}
      {unit}
    />

    <DownloadablePieChart
      title={$_("Investment in agriculture")}
      data={chartIoIAgriculture}
      {unit}
    />

    <DownloadablePieChart
      title={$_("Implementation status")}
      data={chartImpStat}
      {unit}
    />

    <DownloadablePieChart title={$_("Negotiation status")} data={chartNegStat} {unit} />
  </div>
</div>
