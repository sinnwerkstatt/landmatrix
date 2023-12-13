<script lang="ts">
  import type { GeoJSON, Map } from "leaflet"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/newtypes"
  import { createLegend } from "$lib/utils/location"

  import NanoIDField from "$components/Fields/Display2/NanoIDField.svelte"
  import PointField from "$components/Fields/Display2/PointField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  export let version: DealVersion2

  let map: Map

  let selectedEntryId: string | undefined
  $: selectedEntryId = $page.url.hash.split("/")?.[1]

  let locationsCopy: Location[]
  // $: locationsCopy = createEnhancedLocationsCopy(deal.locations)

  // $: {
  //   locationsCopy = []
  //   deal.locations.forEach(loc => {
  //
  //   })
  // }

  let geoJsonLayer: GeoJSON
  let currentLocation: string | undefined

  // const updateGeoJsonLayer = () => {
  //   if (geoJsonLayer) {
  //     map.removeLayer(geoJsonLayer)
  //   }
  //
  //   geoJsonLayer = geoJson(
  //     createLocationFeatures(locationsCopy),
  //     createGeoJsonOptions({
  //       getCurrentLocation: () => currentLocation,
  //       setCurrentLocation: (locationId: string) => goto(`#locations/${locationId}`),
  //     }),
  //   )
  //
  //   map.addLayer(geoJsonLayer)
  // }
  // const updateGeoJsonBounds = () => {
  //   const bounds = currentLocation
  //     ? geoJson(
  //         geoJsonLayer
  //           .getLayers()
  //           .filter(l => l.feature.properties.id === currentLocation)
  //           .map(l => l.feature),
  //       ).getBounds()
  //     : geoJsonLayer.getBounds()
  //   if (bounds.isValid()) {
  //     map.fitBounds(padBounds(bounds), { duration: 1 })
  //   }
  // }

  // // respond to changes in currentLocation
  // $: if (map) {
  //   if (currentLocation) {
  //     updateGeoJsonLayer()
  //     updateGeoJsonBounds()
  //   } else {
  //     updateGeoJsonLayer()
  //     updateGeoJsonBounds()
  //   }
  // }

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail
    map.addControl(createLegend())
  }
  //
  // const onToggleVisibility = (
  //   e: CustomEvent<{ locationId: string; featureId: string }>,
  // ) => {
  //   const { locationId, featureId } = e.detail
  //
  //   locationsCopy = R.adjust(
  //     locationsCopy.findIndex(loc => loc.id === locationId),
  //     toggleFeatureVisibility(featureId),
  //     locationsCopy,
  //   )
  //   updateGeoJsonLayer()
  // }
</script>

<section class="flex flex-wrap">
  <div class="max-h-[75vh] w-full overflow-y-auto p-2 lg:w-1/2">
    {#if version.locations.length > 0}
      <section class="w-full">
        {#each version.locations as location, index}
          <div
            id={location.nid}
            class="p-2 {selectedEntryId === location.nid
              ? 'animate-fadeToWhite dark:animate-fadeToGray'
              : ''}"
          >
            <h3>
              <a href={$page.url.hash.split("/")[0] + `/${location.nid}`}>
                {index + 1}. {$_("Location")}
              </a>
            </h3>
            <NanoIDField
              label={$_("ID")}
              value={location.nid}
              fieldname="location.nid"
            />
            <TextField
              label={$_("Spatial accuracy level")}
              value={location.level_of_accuracy}
              fieldname="location.level_of_accuracy"
              choices={$fieldChoices.deal.level_of_accuracy}
            />
            <TextField
              label={$_("Location")}
              value={location.name}
              fieldname="location.name"
            />
            <PointField
              label={$_("Point")}
              value={location.point}
              fieldname="location.point"
            />

            <TextField
              label={$_("Description")}
              value={location.description}
              fieldname="location.description"
            />
            <TextField
              label={$_("Facility name")}
              value={location.facility_name}
              fieldname="location.facility_name"
            />
            <TextField
              label={$_("Comment")}
              value={location.comment}
              fieldname="location.comment"
            />
          </div>
        {/each}
      </section>
    {/if}
  </div>
  <div class="min-h-[20rem] w-full p-2 lg:w-1/2">
    <BigMap
      containerClass="min-h-full h-full"
      on:ready={onMapReady}
      options={{ center: [0, 0] }}
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
