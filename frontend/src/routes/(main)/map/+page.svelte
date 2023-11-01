<script lang="ts">
  import { queryStore } from "@urql/svelte"
  import type { LeafletEvent, Map, Marker, FeatureGroup } from "leaflet"
  import { divIcon, featureGroup, marker, popup } from "leaflet?client"
  import * as R from "ramda"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import type { OperationResultStore } from "@urql/svelte"

  import { page } from "$app/stores"

  import { dealsQuery } from "$lib/dealQueries"
  import { filters, publicOnly } from "$lib/filters"
  import { countries, loading, regions, isMobile } from "$lib/stores"
  import type { Deal, Location } from "$lib/types/deal"
  import type { Country } from "$lib/types/wagtail"
  import type { GQLFilter } from "$lib/types/filters"

  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DataContainer from "$components/Data/DataContainer.svelte"
  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import BigMap from "$components/Map/BigMap.svelte"
  import {
    getContextLayers,
    visibleContextLayers,
    visibleLayer,
    getBaseLayers,
  } from "$components/Map/layers"
  import {
    displayDealsCount,
    LMCircleClass,
    styleCircle,
  } from "$components/Map/map_helper"
  import MapMarkerPopup from "$components/Map/MapMarkerPopup.svelte"

  interface MyMarker extends Marker {
    deal: Deal
    region_id: number
    country_id: number
    deal_size: number
    loc: Location
    deal_id: number
  }
  interface CountryWCoords extends Country {
    point_lat: number
    point_lon: number
  }

  const ZOOM_LEVEL = {
    REGION_CLUSTERS: 2,
    COUNTRY_CLUSTERS: 3,
    DEAL_CLUSTERS: 5,
    DEAL_PINS: 8,
  }
  const REGION_COORDINATES: { [key: number]: [number, number] } = {
    2: [6.06433, 17.082249],
    9: [-22.7359, 140.0188],
    21: [54.526, -105.2551],
    142: [34.0479, 100.6197],
    150: [52.0055, 37.9587],
    419: [-4.442, -61.3269],
  }

  let bigmap: Map
  let markers: MyMarker[] = []

  let current_zoom: number

  let markersFeatureGroup: FeatureGroup
  let skipMapRefresh = false

  type Subset = "UNFILTERED" | "ACTIVE" | "PUBLIC"

  let deals: OperationResultStore
  $: deals = queryStore<{ deals: Deal[] }, { filters: GQLFilter[]; subset: Subset }>({
    client: $page.data.urqlClient,
    query: dealsQuery,
    variables: {
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    },
  })
  $: loading.set($deals?.fetching ?? false)

  function generateCountryCoords(countries: CountryWCoords[]): {
    [key: number]: [number, number]
  } {
    let ret: { [p: number]: [number, number] } = {}
    countries.forEach(c => (ret[c.id as number] = [c.point_lat, c.point_lon]))
    return ret
  }

  $: country_coords = generateCountryCoords($countries as CountryWCoords[])

  function bigMapIsReady(evt: CustomEvent<Map>) {
    if (import.meta.env.SSR) return
    bigmap = evt.detail
    bigmap.on("zoomend", () => refreshMap())
    bigmap.on("moveend", () => refreshMap())
    markersFeatureGroup = featureGroup()
    bigmap.addLayer(markersFeatureGroup)
    refreshMap()
    flyToCountryOrRegion($filters.country_id, $filters.region_id)
  }

  function refreshMap() {
    if (
      !bigmap ||
      $deals?.data?.deals?.length === 0 ||
      markers.length === 0 ||
      skipMapRefresh
    ) {
      return
    }
    markersFeatureGroup?.clearLayers()
    current_zoom = bigmap.getZoom()

    if (current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !$filters.country_id) {
      // cluster by Region
      Object.entries(
        R.groupBy(R.pipe(R.prop("region_id"), R.toString), markers),
      ).forEach(([key, val]) => {
        if (key === "undefined") return
        let circle = marker(REGION_COORDINATES[+key], {
          icon: divIcon({ className: LMCircleClass }),
        })
        circle.on("click", () => ($filters.region_id = +key))

        markersFeatureGroup.addLayer(circle)

        styleCircle(
          circle,
          $displayDealsCount
            ? val.length
            : val.map(m => m.deal_size).reduce((x, y) => x + y, 0),
          $regions.find(r => r.id === +key)?.name ?? "",
          $displayDealsCount,
        )
      })
    } else if (
      current_zoom < ZOOM_LEVEL.DEAL_CLUSTERS &&
      Object.keys(country_coords).length
    ) {
      // cluster by country
      Object.entries(
        R.groupBy(R.pipe(R.prop("country_id"), R.toString), markers),
      ).forEach(([key, val]) => {
        if (key === "undefined") return
        let circle = marker(country_coords[+key], {
          icon: divIcon({ className: LMCircleClass }),
        })
        circle.on("click", () => ($filters.country_id = +key))
        markersFeatureGroup.addLayer(circle)

        styleCircle(
          circle,
          $displayDealsCount
            ? val.length
            : val.map(m => m.deal_size).reduce((x, y) => x + y, 0),
          $countries.find(c => c.id === +key)?.name ?? "",
          $displayDealsCount,
        )
      })
    } else {
      // show all deals
      const mapBounds = bigmap.getBounds()
      Object.entries(
        R.groupBy(R.pipe(R.prop("country_id"), R.toString), markers),
      ).forEach(([key, val]) => {
        if (key === "undefined") return
        val.forEach(mark => {
          if (mapBounds.contains(mark.getLatLng())) markersFeatureGroup.addLayer(mark)
          else markersFeatureGroup.removeLayer(mark)
        })
      })
    }
  }

  let _dealLocationMarkersCache: { [key: number]: MyMarker[] } = {}

  interface LocWithPoint extends Location {
    point: {
      lat: number
      lng: number
    }
  }

  async function refreshMarkers() {
    if (import.meta.env.SSR) return
    markers = []
    for (let deal of $deals?.data?.deals ?? []) {
      if (!(deal.id in _dealLocationMarkersCache))
        _dealLocationMarkersCache[deal.id] = deal.locations
          .filter(
            (loc: Location): loc is LocWithPoint =>
              !!loc.point && !!loc.point.lng && !!loc.point.lat,
          )
          .map((loc: LocWithPoint) => {
            let myMarker = marker([loc.point.lat, loc.point.lng]) as MyMarker
            myMarker.deal = deal
            myMarker.loc = loc
            myMarker.deal_id = deal.id
            myMarker.deal_size = deal.deal_size
            if (deal.country) {
              myMarker.region_id = deal.country.region.id
              myMarker.country_id = deal.country.id
            }
            myMarker.on("click", createMarkerPopup)
            return myMarker
          })

      markers.push(..._dealLocationMarkersCache[deal.id])
    }
    refreshMap()
  }

  async function createMarkerPopup(event: LeafletEvent) {
    const myMarker = event.target as MyMarker

    const markerContainerDiv = document.createElement("div")
    new MapMarkerPopup({
      target: markerContainerDiv,
      props: { deal: myMarker.deal, location: myMarker.loc },
    })
    popup()
      .setContent(markerContainerDiv)
      .setLatLng(myMarker.getLatLng())
      .openOn(bigmap)
  }

  async function flyToCountryOrRegion(country_id?: number, region_id?: number) {
    if (import.meta.env.SSR || !bigmap) return
    let coords: [number, number] = [0, 0]
    let zoom = ZOOM_LEVEL.REGION_CLUSTERS
    if (country_id) {
      coords = country_coords[country_id]
      zoom = ZOOM_LEVEL.DEAL_CLUSTERS
    } else if (region_id) {
      coords = REGION_COORDINATES[region_id]
      zoom = ZOOM_LEVEL.COUNTRY_CLUSTERS
    }
    if (zoom < current_zoom) {
      // zooming out, apply filter after flying to avoid loading of pins for entire region
      skipMapRefresh = true
      bigmap.flyTo(coords, zoom)
      setTimeout(() => {
        skipMapRefresh = false
        refreshMap()
      }, 1000)
    } else {
      // zooming in, apply filter before flying
      refreshMap()
      setTimeout(() => bigmap.flyTo(coords, zoom), 700)
    }
  }

  $: markersRefreshUnsubscribe = deals?.subscribe(() => refreshMarkers())
  const displayDealsCountUnsubscribe = displayDealsCount.subscribe(() => refreshMap())
  $: flyToCountryOrRegion($filters.country_id, $filters.region_id)

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })

  onDestroy(() => {
    markersRefreshUnsubscribe()
    displayDealsCountUnsubscribe()
  })
</script>

<DataContainer>
  <div class="h-full w-full">
    <BigMap
      containerClass="min-h-full h-full"
      on:ready={bigMapIsReady}
      options={{
        minZoom: ZOOM_LEVEL.REGION_CLUSTERS,
        zoom: ZOOM_LEVEL.REGION_CLUSTERS,
        zoomControl: false,
        //gestureHandling: false,
        center: [12, 30],
      }}
      showLayerSwitcher={false}
    />
  </div>

  <div slot="FilterBar">
    <h4>{$_("Map settings")}</h4>
    <FilterCollapse expanded title={$_("Displayed data")}>
      <label class="block">
        <input
          bind:group={$displayDealsCount}
          class="radio-btn"
          type="radio"
          value={true}
        />
        {$_("Number of deal locations")}
      </label>
      <label class="block">
        <input
          bind:group={$displayDealsCount}
          class="radio-btn"
          type="radio"
          value={false}
        />
        {$_("Area (ha)")}
      </label>
    </FilterCollapse>
    <FilterCollapse expanded title={$_("Base layer")}>
      {#each getBaseLayers($_) as layer}
        <label class="block">
          <input
            type="radio"
            bind:group={$visibleLayer}
            value={layer.id}
            class="radio-btn"
          />
          {layer.name}
        </label>
      {/each}
    </FilterCollapse>

    <FilterCollapse title={$_("Context layers")}>
      {#each getContextLayers($_) as layer}
        <label class="block">
          <input
            type="checkbox"
            bind:group={$visibleContextLayers}
            value={layer.id}
            class="checkbox-btn"
          />
          {layer.name}
          {#if $visibleContextLayers.includes(layer.id)}
            <img
              alt="Legend for {layer.name}"
              src={layer.legendUrlFunction()}
              class="mb-4 ml-4 mt-2 border"
              loading="lazy"
            />
          {/if}
        </label>
      {/each}
    </FilterCollapse>
  </div>
</DataContainer>
