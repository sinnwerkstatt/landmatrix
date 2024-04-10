<script lang="ts">
  import type { Point } from "geojson"
  import type { FeatureGroup, LeafletEvent, Map, Marker } from "leaflet"
  import { divIcon, featureGroup, marker, popup } from "leaflet?client"
  import * as R from "ramda"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { filters } from "$lib/filters"
  import type { components } from "$lib/openAPI"
  import { dealsNG } from "$lib/stores"
  import { isMobile, loading } from "$lib/stores/basics"
  import { Location2, type DealHull } from "$lib/types/newtypes"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import BigMap from "$components/Map/BigMap.svelte"
  import {
    getBaseLayers,
    getContextLayers,
    visibleContextLayers,
    visibleLayer,
  } from "$components/Map/layers"
  import {
    displayDealsCount,
    LMCircleClass,
    styleCircle,
  } from "$components/Map/map_helper"
  import MapMarkerPopup from "$components/Map/MapMarkerPopup.svelte"

  type Country = components["schemas"]["Country"]

  interface MyMarker extends Marker {
    deal: DealHull
    country_id: number
    region_id: number | null
    deal_size: number | null
    loc: Location2
    deal_id: number
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

  function generateCountryCoords(countries: Country[]): {
    [key: number]: [number, number]
  } {
    let ret: { [p: number]: [number, number] } = {}
    countries.forEach(c => (ret[c.id as number] = [c.point_lat, c.point_lon]))
    return ret
  }

  $: country_coords = generateCountryCoords($page.data.countries as Country[])

  function bigMapIsReady(evt: CustomEvent<Map>) {
    if (!browser) return
    bigmap = evt.detail
    bigmap.on("zoomend", () => refreshMap())
    bigmap.on("moveend", () => refreshMap())
    markersFeatureGroup = featureGroup()
    bigmap.addLayer(markersFeatureGroup)
    refreshMap()
    flyToCountryOrRegion($filters.country_id, $filters.region_id)
  }

  const refreshMap = (): void => {
    if (!bigmap || $dealsNG.length === 0 || markers.length === 0 || skipMapRefresh) {
      return
    }
    markersFeatureGroup?.clearLayers()
    current_zoom = bigmap.getZoom()

    const regionIdAsKey: (deal: DealHull) => string = R.pipe(
      R.path(["country", "region", "id"]),
      R.toString,
    )
    const countryIdAsKey: (deal: DealHull) => string = R.pipe(
      R.path(["country", "id"]),
      R.toString,
    )
    const totalDealSize = R.reduce<DealHull, number>(
      (acc, deal) => acc + (deal.selected_version.deal_size ?? 0),
      0,
    )

    if (current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !$filters.country_id) {
      // cluster by LM region
      R.pipe(
        R.groupBy(regionIdAsKey),
        R.forEachObjIndexed((deals, regionId) => {
          if (regionId === "undefined" || !deals) return

          const circle = marker(REGION_COORDINATES[+regionId], {
            icon: divIcon({ className: LMCircleClass }),
          })
          circle.on("click", () => ($filters.region_id = +regionId))
          markersFeatureGroup.addLayer(circle)

          styleCircle(
            circle,
            $displayDealsCount ? deals.length : totalDealSize(deals),
            $page.data.regions.find(r => r.id === +regionId)?.name ?? "",
            $displayDealsCount,
          )
        }),
      )($dealsNG)
    } else if (
      current_zoom < ZOOM_LEVEL.DEAL_CLUSTERS &&
      Object.keys(country_coords).length
    ) {
      // cluster by country
      R.pipe(
        R.groupBy(countryIdAsKey),
        R.forEachObjIndexed((deals, countryId) => {
          if (countryId === "undefined" || !deals) return

          const circle = marker(country_coords[+countryId], {
            icon: divIcon({ className: LMCircleClass }),
          })
          circle.on("click", () => ($filters.country_id = +countryId))
          markersFeatureGroup.addLayer(circle)

          styleCircle(
            circle,
            $displayDealsCount ? deals.length : totalDealSize(deals),
            $page.data.countries.find(c => c.id === +countryId)?.name ?? "",
            $displayDealsCount,
          )
        }),
      )($dealsNG)
    } else {
      // show all deals / markers
      const mapBounds = bigmap.getBounds()
      R.pipe(
        R.groupBy(R.pipe(R.prop("country_id"), R.toString)),
        R.forEachObjIndexed((cMarkers, countryId) => {
          if (countryId === "undefined" || !cMarkers) return
          cMarkers.forEach(mark => {
            if (mapBounds.contains(mark.getLatLng())) {
              markersFeatureGroup.addLayer(mark)
            } else {
              markersFeatureGroup.removeLayer(mark)
            }
          })
        }),
      )(markers)
    }
  }

  let _dealLocationMarkersCache: { [key: number]: MyMarker[] } = {}

  interface LocWithPoint extends Location2 {
    point: Point
  }

  async function refreshMarkers() {
    if (!browser) return
    loading.set(true)
    markers = []
    for (let deal of $dealsNG) {
      if (!(deal.id in _dealLocationMarkersCache))
        _dealLocationMarkersCache[deal.id] = deal.selected_version.locations
          .filter((loc: Location2): loc is LocWithPoint => !!loc.point)
          .map((loc: LocWithPoint) => {
            let myMarker = marker([
              loc.point.coordinates[1],
              loc.point.coordinates[0],
            ]) as MyMarker
            myMarker.deal = deal
            myMarker.loc = loc
            myMarker.deal_id = deal.id
            myMarker.deal_size = deal.selected_version.deal_size
            if (deal.country_id) {
              myMarker.region_id = deal.region_id
              myMarker.country_id = deal.country_id
            }
            myMarker.on("click", createMarkerPopup)
            return myMarker
          })

      markers.push(..._dealLocationMarkersCache[deal.id])
    }

    refreshMap()
    loading.set(false)
  }

  async function createMarkerPopup(event: LeafletEvent) {
    const myMarker = event.target as MyMarker

    const markerContainerDiv = document.createElement("div")
    markerContainerDiv.style.minWidth = "320px"

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
    if (!browser || !bigmap) return
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

  const displayDealsCountUnsubscribe = displayDealsCount.subscribe(() => refreshMap())
  $: $dealsNG && refreshMarkers()
  $: flyToCountryOrRegion($filters.country_id, $filters.region_id)

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })

  onDestroy(() => {
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
    <h2 class="heading5 my-2 px-2">{$_("Map settings")}</h2>
    <!--    <FilterCollapse expanded title={$_("Displayed data")}>-->
    <!--      <label class="block">-->
    <!--        <input-->
    <!--          bind:group={$displayDealsCount}-->
    <!--          name="deals-count-display"-->
    <!--          class="radio-btn"-->
    <!--          type="radio"-->
    <!--          value={true}-->
    <!--        />-->
    <!--        {$_("Number of deal locations")}-->
    <!--      </label>-->
    <!--      <label class="block">-->
    <!--        <input-->
    <!--          bind:group={$displayDealsCount}-->
    <!--          name="deals-count-display"-->
    <!--          class="radio-btn"-->
    <!--          type="radio"-->
    <!--          value={false}-->
    <!--        />-->
    <!--        {$_("Area (ha)")}-->
    <!--      </label>-->
    <!--    </FilterCollapse>-->
    <FilterCollapse expanded title={$_("Base layer")}>
      {#each getBaseLayers($_) as layer}
        <label class="block">
          <input
            type="radio"
            name="base-layer-switch"
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
