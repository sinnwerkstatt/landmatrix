<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { loading } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import DynamicsOfDeal from "$components/Data/Charts/CountryProfile/DynamicsOfDeal.svelte"
  import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte"
  import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"
  import CumulativeNumberOfDeals from "$components/Data/Charts/CountryProfile/CumulativeNumberOfDeals.svelte"
  import CumulativeSizeUnderContract from "$components/Data/Charts/CountryProfile/CumulativeSizeUnderContract.svelte"

  import LandAcquisitionsByCategoryOfProduction from "./land-acquisitions-by-category-of-production/LACOPChart.svelte"

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })
  $: loading.set($deals?.fetching ?? false)
</script>

<svelte:head>
  <title>{$_("Country profile graphs")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div class="h-full w-full overflow-visible">
    {#if $deals.fetching}
      <LoadingPulse />
    {:else if $deals.error}
      <p>Error...{$deals.error.message}</p>
    {:else}
      <div class="flex flex-col md:flex-row">
        <div class="flex-grow">
          <LandAcquisitionsByCategoryOfProduction deals={$deals.data.deals} />
        </div>

        <!--        <CumulativeNumberOfDeals deals={$deals.data.deals} />-->
        <!--        <CumulativeSizeUnderContract deals={$deals.data.deals} />-->
        <!--        <IntentionsPerCategory deals={$deals.data.deals} />-->
        <!--        <LSLAByNegotiation deals={$deals.data.deals} />-->
        <!--        <DynamicsOfDeal deals={$deals.data.deals} />-->
      </div>
    {/if}
  </div>
</ChartsContainer>
