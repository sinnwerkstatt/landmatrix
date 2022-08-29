<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createAgricultureIntentionChartData } from "$lib/data/charts/agricultureIntention"
  import { createImplementationStatusChartData } from "$lib/data/charts/implementationStatus"
  import { createIntentionOfInvestmentGroupChartData } from "$lib/data/charts/intentionOfInvestmentGroup"
  import { createNegotiationStatusChartData } from "$lib/data/charts/negotiationStatusGroup"
  import type { Deal } from "$lib/types/deal"

  import StatusPieChart from "$components/StatusPieChart.svelte"

  export let deals: Deal[] = []
  export let displayDealsCount = false

  $: sortBy = displayDealsCount ? "count" : "size"
  $: unit = displayDealsCount ? "deals" : "ha"

  $: chartImpStat = createImplementationStatusChartData(deals, sortBy)
  $: chartNegStat = createNegotiationStatusChartData(deals, sortBy)
  $: chartIoI = createIntentionOfInvestmentGroupChartData(deals, sortBy)
  $: chartIoIAgriculture = createAgricultureIntentionChartData(deals, sortBy)

  // const rootStyles = getComputedStyle(document.body);
  // const orange = rootStyles.getPropertyValue("--color-lm-orange");
  // console.log("orange", orange);
</script>

<div>
  <div class="grid grid-cols-2 grid-rows-2 gap-4">
    <div>
      <h2>{$_("Intention of investment")}</h2>
      <StatusPieChart data={chartIoI} {unit} />
    </div>
    <div>
      <h2>{$_("Investment in agriculture")}</h2>
      <StatusPieChart data={chartIoIAgriculture} {unit} />
    </div>
    <div>
      <h2>{$_("Implementation status")}</h2>
      <StatusPieChart data={chartImpStat} {unit} />
    </div>
    <div>
      <h2>{$_("Negotiation status")}</h2>
      <StatusPieChart data={chartNegStat} {unit} />
    </div>
  </div>
</div>
