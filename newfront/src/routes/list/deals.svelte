<script lang="ts">
  import VirtualList from "@sveltejs/svelte-virtual-list";
  import { request } from "graphql-request";
  import { GQLEndpoint } from "$lib";
  import { filters, publicOnly } from "$lib/filters";
  import { user } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import { data_deal_query_gql } from "./query";

  export let deals: Deal[] = [];

  $: variables = {
    limit: 0,
    filters: $filters.toGQLFilterArray(),
    subset: $user?.is_authenticated ? ($publicOnly ? "PUBLIC" : "ACTIVE") : "PUBLIC",
  };

  $: request(GQLEndpoint, data_deal_query_gql, variables).then(
    (ret) => (deals = ret.deals)
  );

  // async function fetchDeals() {
  //   const ret = await request(GQLEndpoint, data_deal_query_gql, variables);
  //   deals = ret.deals;
  // }
  // onMount(() => {
  //   fetchDeals();
  // });
</script>

<DataContainer>
  <div class="h-full flex">
    <div
      class="flex-none h-full min-h-[3px] {$showFilterBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />

    <div class="p-4 bg-green-300 w-full">
      {deals.length}
      <VirtualList items={deals} let:item>
        <p>{item.id}: {item.country.name}</p>
      </VirtualList>
    </div>
    <div
      class="flex-none h-full min-h-[3px] {$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />
  </div>
</DataContainer>
