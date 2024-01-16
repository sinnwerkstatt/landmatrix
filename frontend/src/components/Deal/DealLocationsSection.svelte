<script lang="ts">
  import type { GeoJSON, Map } from "leaflet"
  import { geoJson } from "leaflet?client"
  import * as R from "ramda"

  import { goto } from "$app/navigation"

  import type { Deal, Location } from "$lib/types/deal"
  import {
    createEnhancedLocationsCopy,
    createGeoJsonOptions,
    createLegend,
    createLocationFeatures,
    padBounds,
    toggleFeatureVisibility,
  } from "$lib/utils/location"

  import BigMap from "$components/Map/BigMap.svelte"

  export let deal: Deal

  let map: Map

  let locationsCopy: Location[]
  $: locationsCopy = createEnhancedLocationsCopy(deal.locations)

  let geoJsonLayer: GeoJSON
  let currentLocation: string | undefined

  const updateGeoJsonLayer = () => {
    if (geoJsonLayer) {
      map.removeLayer(geoJsonLayer)
    }

    geoJsonLayer = geoJson(
      createLocationFeatures(locationsCopy),
      createGeoJsonOptions({
        getCurrentLocation: () => currentLocation,
        setCurrentLocation: (locationId: string) => goto(`#locations/${locationId}`),
      }),
    )

    map.addLayer(geoJsonLayer)
  }
  const updateGeoJsonBounds = () => {
    const bounds = currentLocation
      ? geoJson(
          geoJsonLayer
            .getLayers()
            .filter(l => l.feature.properties.id === currentLocation)
            .map(l => l.feature),
        ).getBounds()
      : geoJsonLayer.getBounds()
    if (bounds.isValid()) {
      map.fitBounds(padBounds(bounds), { duration: 1 })
    }
  }

  // respond to changes in currentLocation
  $: if (map) {
    if (currentLocation) {
      updateGeoJsonLayer()
      updateGeoJsonBounds()
    } else {
      updateGeoJsonLayer()
      updateGeoJsonBounds()
    }
  }

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail
    map.addControl(createLegend())
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
    updateGeoJsonLayer()
  }
</script>

<section class="flex">
  <div class="max-h-[75vh] w-full overflow-y-auto p-2 lg:w-1/2">
    <!--    <DealSubmodelSection-->
    <!--      bind:selectedEntryId={currentLocation}-->
    <!--      model="location"-->
    <!--      modelName="Location"-->
    <!--      entries={locationsCopy}-->
    <!--      on:toggleVisibility={onToggleVisibility}-->
    <!--    />-->
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
