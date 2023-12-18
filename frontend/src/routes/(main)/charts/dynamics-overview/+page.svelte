<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { chartDescriptions, dealsNG, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"
  import { displayDealsCount } from "$components/Map/map_helper"

  import AgricultureIntentionChart from "./AgricultureIntentionChart.svelte"
  import ImplementationStatusChart from "./ImplementationStatusChart.svelte"
  import IoIGroupChart from "./IoIGroupChart.svelte"
  import NegotiationStatusGroupChart from "./NegotiationStatusGroupChart.svelte"

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
</script>

<svelte:head>
  <title>{$_("Dynamics overview")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div slot="ContextBar">
    <h2 class="heading4 text-gray-700">{$_("Dynamics overview charts")}</h2>
    <div>{@html $chartDescriptions?.dynamics_overview ?? ""}</div>
    <DealDisplayToggle />
  </div>

  {#if $dealsNG.length === 0}
    <LoadingPulse />
  {:else}
    <div class="mx-8 grid grid-rows-1 gap-8 md:mx-32 md:grid-cols-2 md:gap-x-32">
      <IoIGroupChart deals={$dealsNG} displayDealsCount={$displayDealsCount} />
      <AgricultureIntentionChart
        deals={$dealsNG}
        displayDealsCount={$displayDealsCount}
      />
      <NegotiationStatusGroupChart
        deals={$dealsNG}
        displayDealsCount={$displayDealsCount}
      />
      <ImplementationStatusChart
        deals={$dealsNG}
        displayDealsCount={$displayDealsCount}
      />
    </div>
  {/if}
</ChartsContainer>
