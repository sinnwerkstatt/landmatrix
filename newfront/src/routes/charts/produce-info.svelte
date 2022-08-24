<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { showContextBar } from "$components/Data";

  export const load: Load = async () => {
    showContextBar.set(true);
    return {};
  };
</script>

<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { data_deal_query_gql } from "$lib/deal_queries";
  import { filters, publicOnly } from "$lib/filters";
  import { chartDescriptions } from "$lib/stores";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import ProduceInfoMap from "$components/Data/Charts/ProduceInfoMap.svelte";

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
  <title>{$_("Produce Info Map | Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div slot="ContextBar">
    <h2>{$_("Produce Info Map")}</h2>
    <div>{@html $chartDescriptions?.produce_info_map}</div>
  </div>
  <div class="w-5/6 h-5/6 mt-20">
    {#if $deals.fetching}
      <p>Loading...</p>
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <ProduceInfoMap deals={$deals.data.deals} />
    {/if}
  </div>
</ChartsContainer>
