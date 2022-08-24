<script lang="ts">
  import { queryStore } from "@urql/svelte";
  import type { LeafletEvent, Map, MarkerOptions } from "leaflet";
  import { DivIcon, FeatureGroup, Marker, Popup } from "leaflet?client";
  import { groupBy } from "lodash";
  import { onDestroy } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { data_deal_query_gql } from "$lib/deal_queries";
  import { filters, publicOnly } from "$lib/filters";
  import { countries, loading, regions } from "$lib/stores";
  import type { Location } from "$lib/types/deal";
  import { showContextBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import FilterCollapse from "$components/Data/FilterCollapse.svelte";
  import BigMap from "$components/Map/BigMap.svelte";
  import {
    baseLayers,
    contextLayers,
    visibleContextLayers,
    visibleLayer,
  } from "$components/Map/layers";
  import {
    displayDealsCount,
    LMCircleClass,
    styleCircle,
  } from "$components/Map/map_helper";
  import MapMarkerPopup from "$components/Map/MapMarkerPopup.svelte";

  showContextBar.set(true);

  const ZOOM_LEVEL = {
    REGION_CLUSTERS: 2,
    COUNTRY_CLUSTERS: 3,
    DEAL_CLUSTERS: 5,
    DEAL_PINS: 8,
  };
  const REGION_COORDINATES: { [key: number]: [number, number] } = {
    2: [6.06433, 17.082249],
    9: [-22.7359, 140.0188],
    21: [54.526, -105.2551],
    142: [34.0479, 100.6197],
    150: [52.0055, 37.9587],
    419: [-4.442, -61.3269],
  };

  let bigmap: Map;
  let markers: Marker[] = [];

  let current_zoom: number;

  let markersFeatureGroup: FeatureGroup;
  let skipMapRefresh = false;

  $: deals = queryStore({
    client: $page.data.urqlClient,
    query: data_deal_query_gql,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  });
  $: loading.set($deals?.fetching ?? false);

  $: country_coords = Object.fromEntries(
    $countries.map((c) => [c.id, [c.point_lat, c.point_lon]])
  );

  function bigMapIsReady(map) {
    if (import.meta.env.SSR) return;
    // console.log("The big map is ready.");
    bigmap = map.detail;
    bigmap.on("zoomend", () => refreshMap());
    bigmap.on("moveend", () => refreshMap());
    markersFeatureGroup = new FeatureGroup();
    bigmap.addLayer(markersFeatureGroup);
    refreshMap();
    flyToCountryOrRegion($filters.country_id, $filters.region_id);
  }

  function refreshMap() {
    if (!bigmap || skipMapRefresh) return;
    // console.log("Clearing layers");
    markersFeatureGroup?.clearLayers();
    // console.log("Clearing layers: done");
    if ($deals?.data?.deals?.length === 0 || markers.length === 0) return;

    // console.log("Refreshing map");
    current_zoom = bigmap.getZoom();

    if (current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !$filters.country_id) {
      // cluster by Region
      Object.entries(groupBy(markers, (mark) => mark.region_id)).forEach(
        ([key, val]) => {
          if (key === "undefined") return;
          let circle = new Marker(REGION_COORDINATES[key], {
            icon: new DivIcon({ className: LMCircleClass }),
            region_id: key,
          } as MarkerOptions);
          circle.on("click", (e) => ($filters.region_id = +e.target.options.region_id));

          markersFeatureGroup.addLayer(circle);

          styleCircle(
            circle,
            $displayDealsCount
              ? val.length
              : val.reduce((x, y) => {
                  return { deal_size: x.deal_size + y.deal_size };
                }).deal_size,
            $regions.find((r) => r.id === +key).name,
            $displayDealsCount
          );
        }
      );
    } else if (
      current_zoom < ZOOM_LEVEL.DEAL_CLUSTERS &&
      Object.keys(country_coords).length
    ) {
      // cluster by country
      Object.entries(groupBy(markers, (mark) => mark.country_id)).forEach(
        ([key, val]) => {
          // console.log("doing markers for region");
          if (key === "undefined") return;
          let circle = new Marker(country_coords[key], {
            icon: new DivIcon({ className: LMCircleClass }),
            country_id: key,
          });
          circle.on(
            "click",
            (e) => ($filters.country_id = +e.target.options.country_id)
          );
          markersFeatureGroup.addLayer(circle);

          styleCircle(
            circle,
            $displayDealsCount
              ? val.length
              : val.reduce((x, y) => {
                  return { deal_size: x.deal_size + y.deal_size };
                }).deal_size,
            $countries.find((c) => c.id === +key).name,
            $displayDealsCount
          );
        }
      );
    } else {
      // cluster deals with markercluster
      const mapBounds = bigmap.getBounds();
      Object.entries(groupBy(markers, (mark) => mark.country_id)).forEach(
        ([key, val]) => {
          if (key === "undefined") return;
          // let mcluster = new MarkerClusterGroup({ chunkedLoading: true });
          // mcluster.on("clusterclick", (a) => {
          //   let bounds = a.layer.getBounds().pad(0.5);
          //   bigmap.fitBounds(bounds);
          // });
          // val.forEach((mark) => mcluster.addLayer(mark));
          // markersFeatureGroup.addLayer(mcluster);
          val.forEach((mark) => {
            if (mapBounds.contains(mark.getLatLng()))
              markersFeatureGroup.addLayer(mark);
            else markersFeatureGroup.removeLayer(mark);
          });
        }
      );
    }
    // console.log("Refreshing map done.");
  }

  let _dealLocationMarkersCache: { [key: number]: Marker[] } = {};

  async function refreshMarkers() {
    if (import.meta.env.SSR) return;
    // console.log("computing markers ...");
    markers = [];
    for (let deal of $deals?.data?.deals ?? []) {
      if (!(deal.id in _dealLocationMarkersCache))
        _dealLocationMarkersCache[deal.id] = deal.locations
          .filter((loc: Location) => !!loc.point)
          .map((loc: Location) => {
            let marker = new Marker([loc.point.lat, loc.point.lng]);
            marker.deal = deal;
            marker.loc = loc;
            marker.deal_id = deal.id;
            marker.deal_size = deal.deal_size;
            if (deal.country) {
              marker.region_id = deal.country.region.id;
              marker.country_id = deal.country.id;
            }
            marker.on("click", createMarkerPopup);
            return marker;
          });

      markers.push(..._dealLocationMarkersCache[deal.id]);
    }
    // console.log(`computing markers: done - ${markers.length}`);
    refreshMap();
  }

  async function createMarkerPopup(event: LeafletEvent) {
    const marker = event.target as Marker;

    const markerContainerDiv = document.createElement("div");
    new MapMarkerPopup({
      target: markerContainerDiv,
      props: { deal: marker.deal, location: marker.loc },
    });
    new Popup()
      .setContent(markerContainerDiv)
      .setLatLng(marker.getLatLng())
      .openOn(bigmap);
  }

  async function flyToCountryOrRegion(country_id?: number, region_id?: number) {
    if (import.meta.env.SSR || !bigmap) return;
    // console.log("Flying to country or region now");
    let coords: [number, number] = [0, 0];
    let zoom = ZOOM_LEVEL.REGION_CLUSTERS;
    if (country_id) {
      coords = country_coords[country_id];
      zoom = ZOOM_LEVEL.DEAL_CLUSTERS;
    } else if (region_id) {
      coords = REGION_COORDINATES[region_id];
      zoom = ZOOM_LEVEL.COUNTRY_CLUSTERS;
    }
    if (zoom < current_zoom) {
      // zooming out, apply filter after flying to avoid loading of pins for entire region
      skipMapRefresh = true;
      bigmap.flyTo(coords, zoom);
      setTimeout(() => {
        skipMapRefresh = false;
        refreshMap();
      }, 1000);
    } else {
      // zooming in, apply filter before flying
      refreshMap();
      setTimeout(() => bigmap.flyTo(coords, zoom), 700);
    }
  }

  $: markersRefreshUnsubscribe = deals?.subscribe(() => refreshMarkers());
  const displayDealsCountUnsubscribe = displayDealsCount.subscribe(() => refreshMap());
  $: flyToCountryOrRegion($filters.country_id, $filters.region_id);

  onDestroy(() => {
    markersRefreshUnsubscribe();
    displayDealsCountUnsubscribe();
  });
</script>

<DataContainer>
  <div class="h-full w-full">
    <BigMap
      options={{
        minZoom: ZOOM_LEVEL.REGION_CLUSTERS,
        zoom: ZOOM_LEVEL.REGION_CLUSTERS,
        zoomControl: false,
        //gestureHandling: false,
        center: [12, 30],
      }}
      containerClass="min-h-full h-full"
      showLayerSwitcher={false}
      on:ready={bigMapIsReady}
    />
  </div>

  <div slot="FilterBar">
    <h4>{$_("Map settings")}</h4>
    <FilterCollapse expanded title={$_("Displayed data")}>
      <label class="block">
        <input
          type="radio"
          bind:group={$displayDealsCount}
          value={true}
          class="radio-btn"
        />
        {$_("Number of deal locations")}
      </label>
      <label class="block">
        <input
          type="radio"
          bind:group={$displayDealsCount}
          value={false}
          class="radio-btn"
        />
        {$_("Area (ha)")}
      </label>
    </FilterCollapse>
    <FilterCollapse expanded title={$_("Base layer")}>
      {#each baseLayers as layer}
        <label class="block">
          <input
            type="radio"
            bind:group={$visibleLayer}
            value={layer.name}
            class="radio-btn"
          />
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
            class="checkbox-btn"
          />
          {$_(layer.name)}
          {#if $visibleContextLayers.includes(layer.name)}
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
