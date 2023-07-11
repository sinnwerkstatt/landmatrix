<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { chartDescriptions } from "$lib/stores"

  import { showContextBar } from "$components/Data/stores"
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import ProduceInfoMap from "$components/Data/Charts/ProduceInfoMap.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })
  onMount(() => showContextBar.set(true))

  const title = $_("Produce info map")
</script>

<svelte:head>
  <title>{title} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div slot="ContextBar">
    <h2>{title}</h2>
    <div>{@html $chartDescriptions?.produce_info_map}</div>
  </div>
  <div class="mt-20 h-5/6 w-5/6">
    {#if $deals.fetching}
      <LoadingPulse />
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <ProduceInfoMap deals={$deals.data.deals} {title} />
    {/if}
  </div>
</ChartsContainer>
