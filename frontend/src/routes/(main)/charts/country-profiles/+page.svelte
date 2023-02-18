<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { data_deal_query_gql } from "$lib/deal_queries"
  import { filters, publicOnly } from "$lib/filters"
  import { loading } from "$lib/stores"

  import { showContextBar } from "$components/Data/stores"
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import DynamicsOfDeal from "$components/Data/Charts/CountryProfile/DynamicsOfDeal.svelte"
  import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte"
  import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: data_deal_query_gql,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })
  $: loading.set($deals?.fetching ?? false)

  onMount(() => showContextBar.set(false))
</script>

<svelte:head>
  <title>{$_("Country profile graphs")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div
    class="country-profile mt-20 flex w-[clamp(500px,90%,1000px)] flex-col overflow-visible"
  >
    {#if $deals.fetching}
      <LoadingPulse />
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <IntentionsPerCategory deals={$deals.data.deals} />
      <LSLAByNegotiation deals={$deals.data.deals} />
      <DynamicsOfDeal deals={$deals.data.deals} />
    {/if}
  </div>
</ChartsContainer>
