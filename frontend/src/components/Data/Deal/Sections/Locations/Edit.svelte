<script lang="ts">
  import { point } from "@turf/turf"
  import type { Point } from "geojson"
  import { Control, GeoJSON, geoJson, icon, latLngBounds, marker } from "leaflet?client"
  import type { LatLng, Layer, LeafletMouseEvent, Map, Marker } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import {
    Location2,
    type DealHull,
    type PointFeature,
    type PointFeatureProps,
  } from "$lib/types/newtypes"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"
  import { createPointFeatures } from "$lib/utils/location"
  import { padBounds } from "$lib/utils/location.js"

  import LocationLegend from "$components/Data/Deal/Sections/Locations/LocationLegend.svelte"
  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import Entry from "./Entry.svelte"
  import LocationTooltip from "./LocationTooltip.svelte"

  export let deal: DealHull

  let locations = deal.selected_version.locations

  let selectedEntryId: string | undefined
  let activeEntryIdx = 0

  let markerMode = false

  let map: Map | undefined
  let locationsPointLayer: GeoJSON<PointFeatureProps, Point>

  $: label = $_("Location")

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail

    const legend = new Control({ position: "bottomleft" })
    legend.onAdd = () => createComponentAsDiv(LocationLegend)
    map.addControl(legend)

    map.addLayer(locationsPointLayer)

    fitBounds(map)
  }

  $: fitBounds = (map: Map) => {
    let bounds = latLngBounds([])
    map.eachLayer(
      l => (bounds = l instanceof GeoJSON ? l.getBounds().extend(bounds) : bounds),
    )
    map.fitBounds(padBounds(bounds))
  }

  $: if (map && locationsPointLayer) {
    map.removeLayer(locationsPointLayer)
    locationsPointLayer = createLayer(locations)
    map.addLayer(locationsPointLayer)

    fitBounds(map)
  }

  $: if (map && locationsPointLayer) {
    const updateActiveLocationMarker = (event: LeafletMouseEvent) =>
      updateActiveLocationPoint(latLng2Point(event.latlng))

    if (markerMode) {
      map.addEventListener("click", updateActiveLocationMarker)

      locationsPointLayer.eachLayer(layer => {
        const marker = layer as Marker
        if (marker.feature?.properties.id === locations[activeEntryIdx].nid) {
          marker.dragging?.enable()
        }
      })
    } else {
      map.removeEventListener("click", updateActiveLocationMarker)

      locationsPointLayer.eachLayer((layer: Layer) =>
        (layer as Marker).dragging?.disable(),
      )
    }
  }

  $: updateActiveLocationPoint = (point: Point) => {
    deal.selected_version.locations[activeEntryIdx].point = point
  }

  const latLng2Point = (latLng: LatLng): Point => {
    const coords = [latLng.lng, latLng.lat].map(val => parseFloat(val.toFixed(5)))
    return point(coords).geometry
  }

  $: isAnyLocationSelected = (): boolean => selectedEntryId !== undefined
  $: isSelectedLocation = (locationId: string): boolean =>
    selectedEntryId === locationId
  $: getLocationRedirect = (locationId: string): string =>
    `#` + (isSelectedLocation(locationId) ? "" : locationId)
  $: setCurrentLocation = (locationId: string): Promise<void> =>
    goto(getLocationRedirect(locationId))

  $: createLayer = (locations: Location2[]) =>
    geoJson(createPointFeatures(locations), {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        const tooltipElement = createComponentAsDiv(LocationTooltip, { feature })

        layer.bindPopup(tooltipElement, { keepInView: true })
        layer.on("click", () => setCurrentLocation(feature.properties.id))
        layer.on("mouseover", () => layer.openPopup())
        layer.on("mouseout", () => layer.closePopup())
        // layer.on("dragstart", () => console.log("dragstart"))
        layer.on("dragend", () => {
          const point = latLng2Point((layer as Marker).getLatLng())
          updateActiveLocationPoint(point)
        })
      },
      pointToLayer: (feature: PointFeature, latlng) =>
        marker(latlng, {
          icon: icon({
            iconUrl: "/images/marker-icon.png",
            shadowUrl: "/images/marker-shadow.png",
            shadowSize: [0, 0],
            iconAnchor: [12.5, 41],
            popupAnchor: [0, -35],
            className:
              isAnyLocationSelected() && !isSelectedLocation(feature.properties.id)
                ? "leaflet-hidden"
                : "",
          }),
        }),
    })

  onMount(() => {
    locationsPointLayer = createLayer(locations)
  })

  onDestroy(() => {
    if (map && locationsPointLayer) {
      map.removeLayer(locationsPointLayer)
    }
  })
</script>

<form class="grid h-full gap-2 lg:grid-cols-5" id="locations">
  <div class="lg:order-last lg:col-span-2">
    <BigMap
      on:ready={onMapReady}
      options={{ center: [0, 0] }}
      containerClass="h-full min-h-[300px]"
    />
    <!--{#if activeEntryIdx !== -1}-->
    <!--  <div-->
    <!--    class="absolute bottom-2 left-2 {markerMode-->
    <!--      ? 'bg-orange text-white'-->
    <!--      : 'bg-white text-orange'}"-->
    <!--  >-->
    <!--    <button-->
    <!--      type="button"-->
    <!--      class="z-10 rounded border-2 border-black/30 px-2 pb-1.5 pt-0.5"-->
    <!--      on:click={() => {-->
    <!--        markerMode = !markerMode-->
    <!--      }}-->
    <!--      title="Create or move point"-->
    <!--    >-->
    <!--      <LocationDot class="inline h-5 w-5" />-->
    <!--    </button>-->
    <!--  </div>-->
    <!--{/if}-->
  </div>

  <div class="h-full lg:col-span-3 lg:overflow-y-auto">
    <SubmodelEditField
      bind:entries={deal.selected_version.locations}
      bind:selectedEntryId
      entryComponent={Entry}
      createEntry={nid => new Location2(nid)}
      extras={{
        map,
        country: $page.data.countries.find(c => c.id === deal.country_id),
      }}
      {label}
    />
  </div>
</form>

<style>
  :global(img.leaflet-hidden) {
    opacity: 0.6;
    filter: saturate(0);
  }
</style>
