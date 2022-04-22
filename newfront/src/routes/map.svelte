<script lang="ts">
  import { request } from "graphql-request";
  import { GQLEndpoint } from "$lib";
  import { filters, publicOnly } from "$lib/filters";
  import { user } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import BigMap from "$components/Map/BigMap.svelte";
  import { data_deal_query_gql } from "./list/query";

  export let deals: Deal[] = [];
  let bigmap;
  let current_zoom;

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
  function bigMapIsReady(map) {
    console.log("The big map is ready.");
    bigmap = map.detail;
    // bigmap.addLayer(markersFeatureGroup);
    // bigmap.addLayer(contextLayersLayerGroup);
    bigmap.on("zoomend", () => (current_zoom = bigmap.getZoom()));
  }
</script>

<DataContainer>
  <div class="h-full w-full">
    <BigMap
      options={{
        minZoom: 2,
        zoom: 2,
        zoomControl: false,
        gestureHandling: false,
        center: [12, 30],
      }}
      containerClass="min-h-full h-full"
      showLayerSwitcher={false}
      on:ready={bigMapIsReady}
    />
  </div>
</DataContainer>
