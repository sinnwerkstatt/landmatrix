<script lang="ts">
  import { gql, queryStore } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { filters } from "$lib/filters"
  import { chartDescriptions, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import CountryInvestorInfo from "$components/Data/Charts/CountryInvestorInfo.svelte"
  import WebOfTransnationalDeals from "$components/Data/Charts/WebOfTransnationalDeals.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  $: title = $_("Web of transnational deals")

  const transnationalDealsQuery = gql`
    query ($filters: [Filter]) {
      transnational_deals(filters: $filters)
    }
  `

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: transnationalDealsQuery,
    variables: {
      filters: $filters
        .toGQLFilterArray()
        .filter(f => f.field !== "country_id" && f.field !== "country.region_id"),
    },
  })

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
    <WebOfTransnationalDeals {title} deals={$deals.data.transnational_deals} />
  {/if}

  <div slot="ContextBar">
    <h2 class="heading4 text-lm-dark">{title}</h2>
    <div>{@html $chartDescriptions?.web_of_transnational_deals ?? ""}</div>
    <CountryInvestorInfo />
  </div>
</ChartsContainer>
