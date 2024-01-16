<script lang="ts">
  import type { Point } from "geojson"
  import { geoJson, type Layer, type Map } from "leaflet"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import { fieldChoices, geoJsonLayerGroup } from "$lib/stores"
  import type { DealVersion2, Location2, PointFeature } from "$lib/types/newtypes"
  import { createLegend, createTooltip } from "$lib/utils/location"

  import NanoIDField from "$components/Fields/Display2/NanoIDField.svelte"
  import PointField from "$components/Fields/Display2/PointField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasField from "./LocationAreasField.svelte"

  export let version: DealVersion2

  let map: Map | undefined

  let selectedEntryId: string | undefined
  $: selectedEntryId = $page.url.hash.split("/")?.[1]

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail
    map.addControl(createLegend())
  }

  $: setCurrentLocation = (locationId: string) =>
    selectedEntryId === locationId
      ? goto(`#locations`)
      : goto(`#locations/${locationId}`)

  $: isSelectedLocation = (location: Location2) => selectedEntryId === location.nid

  const createPointFeature = (location: Location2): PointFeature => ({
    type: "Feature",
    geometry: location.point as Point,
    properties: {
      id: location.nid,
      level_of_accuracy: location.level_of_accuracy,
      name: location.name,
    },
  })

  const createPointFeatures = (locations: Location2[]): PointFeature[] =>
    locations.filter(l => l.point !== null).map(l => createPointFeature(l))

  const createLayer = (locations: Location2[]) =>
    geoJson(createPointFeatures(locations), {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        layer.bindPopup(createTooltip(feature), { keepInView: true })
        layer.on("click", () => setCurrentLocation(feature.properties.id))
        layer.on("mouseover", () => layer.openPopup())
        layer.on("mouseout", () => layer.closePopup())
      },
    })

  let layer

  $: if ($geoJsonLayerGroup && layer) {
    // console.log("hi locations")
    $geoJsonLayerGroup.removeLayer(layer)
    layer = createLayer(version.locations)
    $geoJsonLayerGroup.addLayer(layer)
  }

  onMount(() => {
    layer = createLayer(version.locations)
  })

  onDestroy(() => {
    if ($geoJsonLayerGroup && layer) {
      $geoJsonLayerGroup.removeLayer(layer)
    }
  })
</script>

<section class="flex flex-wrap lg:h-full">
  <div class="w-full overflow-y-auto p-2 lg:h-full lg:w-2/5">
    {#if version.locations.length > 0}
      {#each version.locations as location, index}
        <article
          id={location.nid}
          class="p-2"
          class:animate-fadeToWhite={isSelectedLocation(location)}
          class:dark:animate-fadeToGray={isSelectedLocation(location)}
        >
          <h3 class="heading4">
            <a href={`#locations/${location.nid}`}>
              {index + 1}. {$_("Location")}
              <small class="text-sm text-gray-500">
                #{location.nid}
              </small>
            </a>
          </h3>
          <!--          <NanoIDField label={$_("ID")} value={location.nid} fieldname="location.nid" />-->
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
          <LocationAreasField
            label={$_("Areas")}
            areas={location.areas}
            locationId={location.nid}
            fieldname="location.areas"
            isSelectedEntry={isSelectedLocation(location)}
          />
        </article>
      {/each}
    {/if}
  </div>
  <div class="h-[600px] w-full p-2 lg:w-3/5">
    <BigMap
      containerClass="min-h-full h-full"
      on:ready={onMapReady}
      options={{ center: [0, 0] }}
    />
  </div>
</section>
