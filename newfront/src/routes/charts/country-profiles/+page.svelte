<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { data_deal_query_gql } from "$lib/deal_queries";
  import { filters, publicOnly } from "$lib/filters";
  import { loading } from "$lib/stores";
  import { showContextBar } from "$components/Data";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import DynamicsOfDeal from "$components/Data/Charts/CountryProfile/DynamicsOfDeal.svelte";
  import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte";
  import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte";

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: data_deal_query_gql,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  });
  $: loading.set($deals?.fetching ?? false);

  onMount(() => showContextBar.set(false));
</script>

<svelte:head>
  <title>{$_("Country profile graphs | Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div
    class="country-profile mt-20 overflow-visible flex flex-col w-[clamp(500px,90%,1000px)]"
  >
    <IntentionsPerCategory deals={$deals?.data?.deals} />
    <LSLAByNegotiation deals={$deals?.data?.deals} />
    <DynamicsOfDeal deals={$deals?.data?.deals} />
  </div>
</ChartsContainer>
