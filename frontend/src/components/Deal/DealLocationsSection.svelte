<script lang="ts">
  import type { Map, GeoJSON } from "leaflet"
  import { geoJson } from "leaflet?client"
  import * as R from "ramda"

  import type { Deal, Location } from "$lib/types/deal"
  import {
    padBounds,
    createEnhancedLocationsCopy,
    createLocationFeatures,
    toggleFeatureVisibility,
    createGeoJsonOptions,
  } from "$lib/utils/location"

  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  export let deal: Deal

  let map: Map

  let locationsCopy: Location[]
  $: locationsCopy = createEnhancedLocationsCopy(deal.locations)

  let geoJsonLayer: GeoJSON
  let currentLocation: string | undefined

  // respond to changes in locationsCopy and currentLocation
  $: if (map) {
    if (geoJsonLayer) {
      map.removeLayer(geoJsonLayer)
    }

    geoJsonLayer = geoJson(
      createLocationFeatures(locationsCopy),
      createGeoJsonOptions({
        getCurrentLocation: () => currentLocation,
        setCurrentLocation: (locationId: string) => {
          currentLocation = locationId
        },
      }),
    )

    map.addLayer(geoJsonLayer)

    const bounds = geoJsonLayer.getBounds()
    if (bounds.isValid()) {
      map.fitBounds(padBounds(bounds), { animate: false })
    }
  }

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail
  }

  const onToggleVisibility = (
    e: CustomEvent<{ locationId: string; featureId: string }>,
  ) => {
    const { locationId, featureId } = e.detail

    locationsCopy = R.adjust(
      locationsCopy.findIndex(loc => loc.id === locationId),
      toggleFeatureVisibility(featureId),
      locationsCopy,
    )
  }
</script>

<section class="flex">
  <div class="max-h-[75vh] w-full overflow-y-auto p-2 lg:w-1/2">
    <DealSubmodelSection
      bind:selectedEntryId={currentLocation}
      model="location"
      modelName="Location"
      entries={locationsCopy}
      on:toggleVisibility={onToggleVisibility}
    />
  </div>
  <div class="min-h-[20rem] w-full p-2 lg:w-1/2">
    <BigMap
      containerClass="min-h-full h-full"
      options={{ center: [0, 0] }}
      on:ready={onMapReady}
    />
  </div>
</section>

<style>
  :global(path.leaflet-hidden) {
    /*display: none;*/
    opacity: 0.5;
    filter: saturate(0);
  }

  :global(img.leaflet-hidden) {
    opacity: 0.6;
    filter: saturate(0);
  }
</style>
