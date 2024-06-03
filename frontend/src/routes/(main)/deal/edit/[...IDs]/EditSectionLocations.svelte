<script lang="ts">
  import { point } from "@turf/turf"
  import type { Point } from "geojson"
  import { GeoJSON, icon, marker } from "leaflet"
  import type { LatLng, Layer, LeafletMouseEvent, Map, Marker } from "leaflet?client"
  import { Control, geoJson } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import type { components } from "$lib/openAPI"
  import {
    Location2,
    type PointFeature,
    type PointFeatureProps,
  } from "$lib/types/newtypes"
  import { isEmptySubmodel } from "$lib/utils/data_processing"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"
  import { createPointFeatures, fitBounds } from "$lib/utils/location"

  import LocationTooltip from "$components/Deal/LocationTooltip.svelte"
  import EditField from "$components/Fields/EditField.svelte"
  import LocationDot from "$components/icons/LocationDot.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasEditField from "./LocationAreasEditField.svelte"

  export let locations: Location2[]
  export let country: components["schemas"]["Country"] | undefined

  let activeEntryIdx = -1
  let markerMode = false

  let map: Map | undefined
  let locationsPointLayer: GeoJSON<PointFeatureProps, Point>

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail

    const legend = new Control({ position: "bottomleft" })
    // legend.onAdd = () => createComponentAsDiv(LocationLegend)
    map.addControl(legend)

    map.addLayer(locationsPointLayer)
    fitBounds(locationsPointLayer, map)
  }

  $: if (map && locationsPointLayer) {
    map.removeLayer(locationsPointLayer)
    locationsPointLayer = createLayer(locations, activeEntryIdx)
    map.addLayer(locationsPointLayer)
    // let bounds = locationsPointLayer.getBounds()
    // map.eachLayer(
    //   l => (bounds = l instanceof GeoJSON ? l.getBounds().extend(bounds) : bounds),
    // )
    // map.fitBounds(bounds)
    fitBounds(locationsPointLayer, map)
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

  const addEntry = () => {
    const currentIDs = locations.map(entry => entry.nid)
    locations = [...locations, new Location2(newNanoid(currentIDs))]
    activeEntryIdx = locations.length - 1
  }

  const toggleActiveEntry = (index: number) => {
    activeEntryIdx = activeEntryIdx === index ? -1 : index
    markerMode = false
  }

  const removeEntry = (c: Location2) => {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Location")} #${c.nid}?`)
      if (!areYouSure) return
    }
    locations = locations.filter(x => x.nid !== c.nid)
    activeEntryIdx = -1
  }

  $: updateActiveLocationPoint = (point: Point) => {
    locations[activeEntryIdx].point = point
  }

  const latLng2Point = (latLng: LatLng): Point => {
    const coords = [latLng.lng, latLng.lat].map(val => parseFloat(val.toFixed(5)))
    return point(coords).geometry
  }

  const createLayer = (locations: Location2[], activeEntryIdx: number) =>
    geoJson(createPointFeatures(locations), {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        const tooltipElement = createComponentAsDiv(LocationTooltip, { feature })
        const locationIndex = locations.findIndex(l => l.nid === feature.properties.id)

        layer.bindPopup(tooltipElement, { keepInView: true })
        layer.on("click", () => toggleActiveEntry(locationIndex))
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
              feature.properties.id === locations[activeEntryIdx]?.nid
                ? ""
                : "leaflet-hidden",
          }),
        }),
    })

  onMount(() => {
    locationsPointLayer = createLayer(locations, activeEntryIdx)
  })

  onDestroy(() => {
    if (map && locationsPointLayer) {
      map.removeLayer(locationsPointLayer)
    }
  })
</script>

<form class="grid h-full grid-cols-5" id="locations">
  <div class="col-span-2 flex h-full flex-col overflow-y-auto p-2">
    <div class="flex flex-row items-center justify-between">
      {#if activeEntryIdx >= 0}
        <h3 class="heading4">
          {activeEntryIdx + 1}. {$_("Location")}
          <small class="text-sm text-gray-500">
            #{locations[activeEntryIdx].nid}
          </small>
        </h3>
        <button
          type="button"
          class="flex-initial p-2"
          on:click={() => removeEntry(locations[activeEntryIdx])}
        >
          <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
        </button>
      {:else}
        <h3 class="heading4">
          {$_("No location selected")}
        </h3>
      {/if}
    </div>
    <div class="flex flex-wrap gap-2 py-2">
      {#each locations as location, index (location.nid)}
        <button
          type="button"
          class="btn-outline"
          class:btn-orange={activeEntryIdx !== index}
          on:click={() => toggleActiveEntry(index)}
          title="#{location.nid}"
        >
          <span class="inline-block h-6 w-6">
            {index + 1}
          </span>
        </button>
      {/each}
      <button
        type="button"
        class="btn-outline btn-orange"
        on:click={addEntry}
        title={$_("Add") + " " + $_("Location")}
      >
        <PlusIcon class="h-6 w-6" />
      </button>
    </div>

    {#if activeEntryIdx >= 0}
      <div
        class="h-full space-y-4 overflow-y-auto pb-52 pt-4"
        transition:slide={{ duration: 200 }}
      >
        <EditField
          fieldname="location.level_of_accuracy"
          bind:value={locations[activeEntryIdx].level_of_accuracy}
          extras={{ required: true }}
          showLabel
        />
        <EditField
          fieldname="location.name"
          bind:value={locations[activeEntryIdx].name}
          extras={{
            countryCode: country?.code_alpha2,
            onGoogleAutocomplete: updateActiveLocationPoint,
          }}
          showLabel
        />
        <EditField
          fieldname="location.point"
          bind:value={locations[activeEntryIdx].point}
          showLabel
        />
        <EditField
          fieldname="location.description"
          bind:value={locations[activeEntryIdx].description}
          showLabel
        />
        <EditField
          fieldname="location.facility_name"
          bind:value={locations[activeEntryIdx].facility_name}
          showLabel
        />
        <EditField
          fieldname="location.comment"
          bind:value={locations[activeEntryIdx].comment}
          showLabel
        />
        <LocationAreasEditField
          bind:areas={locations[activeEntryIdx].areas}
          {map}
          isSelectedEntry
        />
      </div>
    {/if}
  </div>

  <div class="col-span-3 p-2">
    <BigMap on:ready={onMapReady} options={{ center: [0, 0] }}>
      {#if activeEntryIdx !== -1}
        <div
          class="absolute bottom-2 left-2 {markerMode
            ? 'bg-orange text-white'
            : 'bg-white text-orange'}"
        >
          <button
            type="button"
            class="z-10 rounded border-2 border-black/30 px-2 pb-1.5 pt-0.5"
            on:click={() => {
              markerMode = !markerMode
            }}
            title="Create or move point"
          >
            <LocationDot class="inline h-5 w-5" />
          </button>
        </div>
      {/if}
    </BigMap>
  </div>
</form>

<style>
  :global(img.leaflet-hidden) {
    opacity: 0.6;
    filter: saturate(0);
  }
</style>
