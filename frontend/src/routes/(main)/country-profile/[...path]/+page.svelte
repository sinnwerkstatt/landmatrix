<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { loading, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  export let data

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })
  $: loading.set($deals?.fetching ?? false)

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
</script>

<svelte:head>
  <title>{$_("Country profiles")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div class="h-full w-full overflow-visible">
    {#if $deals.fetching}
      <LoadingPulse />
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <svelte:component this={data.component} deals={$deals.data.deals} />
    {/if}
  </div>

  <div slot="ContextBar">
    <h2>{$_("Country profiles")}</h2>
    <DealDisplayToggle />
  </div>
</ChartsContainer>
