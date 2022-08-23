<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { data_deal_query_gql } from "$lib/deal_queries";
  import { filters, publicOnly } from "$lib/filters";
  import { chartDescriptions } from "$lib/stores";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import DynamicsOverview from "$components/Data/Charts/DynamicsOverview.svelte";
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte";
  import { displayDealsCount } from "$components/Map/map_helper";

  $: deals = queryStore({
    client: $page.stuff.urqlClient,
    query: data_deal_query_gql,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  });
</script>

<svelte:head>
  <title>{$_("Dynamics Overview | Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div slot="ContextBar">
    <h2>{$_("Dynamics overview charts")}</h2>
    <div>{@html $chartDescriptions?.dynamics_overview}</div>
    <DealDisplayToggle />
  </div>
  <div class="mt-20">
    {#if $deals.fetching}
      <p>Loading...</p>
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
