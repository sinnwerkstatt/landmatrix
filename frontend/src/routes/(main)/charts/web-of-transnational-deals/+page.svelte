<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import type { EdgeBundlingData } from "$lib/data/charts/webOfTransnationalDeals"
  import { filters, FilterValues, publicOnly } from "$lib/filters"
  import { chartDescriptions } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import CountryInvestorInfo from "$components/Data/Charts/CountryInvestorInfo.svelte"
  import WebOfTransnationalDeals from "$components/Data/Charts/WebOfTransnationalDeals.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  let title = $derived($_("Web of transnational deals"))

  let transnationalDeals: EdgeBundlingData | undefined = $state()

  const fetchTransnationalDeals = async (fltrs: FilterValues) => {
    const f1 = new FilterValues().copyNoCountry(fltrs)

    const subset = $publicOnly ? "PUBLIC" : "ACTIVE"
    const ret = await fetch(
      `/api/charts/web_of_transnational_deals/?subset=${subset}&${f1.toRESTFilterArray()}`,
    )
    transnationalDeals = await ret.json()
  }

  $effect(() => {
    fetchTransnationalDeals($filters)
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
  {#if transnationalDeals === undefined}
    <LoadingPulse />
  {:else}
    <WebOfTransnationalDeals {title} deals={transnationalDeals} />
  {/if}
  {#snippet ContextBar()}
    <div>
      <h2 class="heading5">{title}</h2>
      <div>{@html $chartDescriptions.web_of_transnational_deals}</div>
      <CountryInvestorInfo />
    </div>
  {/snippet}
</ChartsContainer>
