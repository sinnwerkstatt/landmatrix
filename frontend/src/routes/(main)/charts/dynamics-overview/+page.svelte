<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { chartDescriptions, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"
  import { displayDealsCount } from "$components/Map/map_helper"
  import { showContextBar, showFilterBar } from "$components/Data/stores"

  import AgricultureIntentionChart from "./AgricultureIntentionChart.svelte"
  import ImplementationStatusChart from "./ImplementationStatusChart.svelte"
  import IoIGroupChart from "./IoIGroupChart.svelte"
  import NegotiationStatusGroupChart from "./NegotiationStatusGroupChart.svelte"

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })

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
    <h2>{$_("Dynamics overview charts")}</h2>
    <div>{@html $chartDescriptions?.dynamics_overview ?? ""}</div>
    <DealDisplayToggle />
  </div>

  {#if $deals.fetching}
    <LoadingPulse />
  {:else if $deals.error}
    <p>Error...{$deals.error.message}</p>
  {:else}
    <div class="mx-8 grid grid-rows-1 gap-8 md:mx-32 md:grid-cols-2 md:gap-x-32">
      <IoIGroupChart deals={$deals.data.deals} displayDealsCount={$displayDealsCount} />
      <AgricultureIntentionChart
        deals={$deals.data.deals}
        displayDealsCount={$displayDealsCount}
      />
      <NegotiationStatusGroupChart
        deals={$deals.data.deals}
        displayDealsCount={$displayDealsCount}
      />
      <ImplementationStatusChart
        deals={$deals.data.deals}
        displayDealsCount={$displayDealsCount}
      />
    </div>
  {/if}
</ChartsContainer>
