<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { chartDescriptions, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import DynamicsOverview from "$components/Data/Charts/DynamicsOverview.svelte"
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"
  import { displayDealsCount } from "$components/Map/map_helper"
  import { showContextBar, showFilterBar } from "$components/Data/stores"

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
    <div>{@html $chartDescriptions?.dynamics_overview}</div>
    <DealDisplayToggle />
  </div>
  <div class="mt-8">
    {#if $deals.fetching}
      <LoadingPulse />
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <DynamicsOverview
        deals={$deals.data.deals}
        displayDealsCount={$displayDealsCount}
      />
    {/if}
  </div>
</ChartsContainer>
