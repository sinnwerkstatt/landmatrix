<script lang="ts">
  import { request } from "graphql-request";
  import { _ } from "svelte-i18n";
  import { GQLEndpoint } from "$lib";
  import { filters, publicOnly } from "$lib/filters";
  import { user } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import FilterCollapse from "$components/Data/FilterCollapse.svelte";
  import BigMap from "$components/Map/BigMap.svelte";
  import {
    baseLayers,
    contextLayers,
    visibleContextLayers,
    visibleLayer,
  } from "$components/Map/layers";
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

  let displayDealsCount;
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

  <div slot="FilterBar">
    <h4>{$_("Map settings")}</h4>
    <FilterCollapse initExpanded={true} title={$_("Displayed data")}>
      <label class="block">
        <input type="radio" bind:group={displayDealsCount} value={true} />
        {$_("Number of deal locations")}
      </label>
      <label class="block">
        <input type="radio" bind:group={displayDealsCount} value={false} />
        {$_("Area (ha)")}
      </label>
    </FilterCollapse>
    <FilterCollapse initExpanded={true} title={$_("Base layer")}>
      {#each baseLayers as layer}
        <label class="block">
          <input type="radio" bind:group={$visibleLayer} value={layer.name} />
          {$_(layer.name)}
        </label>
      {/each}
    </FilterCollapse>

    <FilterCollapse title={$_("Context layers")}>
      {#each contextLayers as layer}
        <label class="block">
          <input
            type="checkbox"
            bind:group={$visibleContextLayers}
            value={layer.name}
          />
          {$_(layer.name)}
          {#if $visibleContextLayers.includes(layer)}
            <img
              alt="Legend for {layer.name}"
              src={layer.legendUrlFunction()}
              class="context-layer-legend-image"
            />
          {/if}
        </label>
      {/each}
    </FilterCollapse>
  </div>
</DataContainer>
