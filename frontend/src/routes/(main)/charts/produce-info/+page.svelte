<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { chartDescriptions, isMobile } from "$lib/stores"

  import { showContextBar, showFilterBar } from "$components/Data/stores"
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

  $: title = $_("Produce info map")

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
</script>

<svelte:head>
  <title>{title} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  {#if $deals.fetching}
    <LoadingPulse />
  {:else if $deals.error}
    <p>Error...{$deals.error.message}</p>
  {:else}
    <ProduceInfoMap deals={$deals.data.deals} {title} />
  {/if}

  <div slot="ContextBar">
    <h2>{title}</h2>
    <div>{@html $chartDescriptions?.produce_info_map ?? ""}</div>
  </div>
</ChartsContainer>
