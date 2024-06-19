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
    type DealHull,
    type Location2,
    type Mutable,
    type PointFeature,
    type PointFeatureProps,
  } from "$lib/types/data"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"
  import { createPointFeatures, padBounds } from "$lib/utils/location"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"
  import LocationDot from "$components/icons/LocationDot.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import Entry from "./Entry.svelte"
  import LocationLegend from "./LocationLegend.svelte"
  import { createLocation, isEmptyLocation } from "./locations"
  import LocationTooltip from "./LocationTooltip.svelte"

  export let deal: Mutable<DealHull>

  let selectedEntryId: string | undefined

  const getSelectedEntryIndex = () =>
    locations.findIndex(l => l.nid === selectedEntryId)

  let markerMode = false

  let map: Map | undefined
  let locationsPointLayer: GeoJSON<PointFeatureProps, Point>

  $: label = $_("Location")
  $: locations = deal.selected_version.locations

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail

    const legend = new Control({ position: "bottomright" })
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
    if (bounds.isValid()) {
      map.fitBounds(padBounds(bounds))
    }
  }

  $: if (map && locationsPointLayer) {
    map.removeLayer(locationsPointLayer)
    locationsPointLayer = createLayer(locations)
    map.addLayer(locationsPointLayer)

    fitBounds(map)
  }

  const updateActiveLocationMarker = (event: LeafletMouseEvent) =>
    updateActiveLocationPoint(latLng2Point(event.latlng))

  $: if (map && locationsPointLayer) {
    if (selectedEntryId && markerMode) {
      map.addEventListener("click", updateActiveLocationMarker)

      const selectedEntryIndex = getSelectedEntryIndex()

      locationsPointLayer.eachLayer(layer => {
        const marker = layer as Marker
        if (marker.feature?.properties.id === locations[selectedEntryIndex].nid) {
          marker.dragging?.enable()
        }
      })
    } else {
      markerMode = false

      map.removeEventListener("click", updateActiveLocationMarker)

      locationsPointLayer.eachLayer((layer: Layer) =>
        (layer as Marker).dragging?.disable(),
      )
    }
  }

  $: updateActiveLocationPoint = (point: Point) => {
    const selectedEntryIndex = getSelectedEntryIndex()
    deal.selected_version.locations[selectedEntryIndex].point = point
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
    >
      {#if selectedEntryId}
        <div
          class="absolute bottom-[10px] left-[10px] {markerMode
            ? 'bg-orange text-white'
            : 'bg-white text-orange'}"
        >
          <button
            type="button"
            class="z-10 h-[40px] w-[40px] rounded border-2 border-black/30 px-2 pb-1.5 pt-0.5"
            on:click={() => {
              markerMode = !markerMode
            }}
            title={$_("Create or move point")}
          >
            <LocationDot class="inline h-5 w-5" />
          </button>
        </div>
      {/if}
    </BigMap>
  </div>

  <div class="h-full lg:col-span-3 lg:overflow-y-auto">
    <SubmodelEditField
      bind:entries={deal.selected_version.locations}
      bind:selectedEntryId
      entryComponent={Entry}
      createEntry={createLocation}
      isEmpty={isEmptyLocation}
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
