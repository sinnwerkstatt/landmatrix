<script lang="ts">
  import type { Point } from "geojson"
  import type { GeoJSON, Layer, Map } from "leaflet"
  import { Control, geoJson } from "leaflet"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import type {
    DealVersion2,
    Location2,
    PointFeature,
    PointFeatureProps,
  } from "$lib/types/newtypes"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"
  import { createPointFeatures, fitBounds } from "$lib/utils/location"

  import LocationLegend from "$components/Deal/LocationLegend.svelte"
  import LocationTooltip from "$components/Deal/LocationTooltip.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasField from "./LocationAreasField.svelte"

  export let data

  let version: DealVersion2 = data.deal.selected_version
  $: version = data.deal.selected_version

  let map: Map | undefined
  let locationsPointLayer: GeoJSON<PointFeatureProps, Point>

  let selectedLocationId: string | null = null
  $: selectedLocationId = $page.url.hash?.replace("#", "")

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail

    const legend = new Control({ position: "bottomleft" })
    legend.onAdd = () => createComponentAsDiv(LocationLegend)
    map.addControl(legend)

    map.addLayer(locationsPointLayer)
    fitBounds(locationsPointLayer, map)
  }

  $: isSelectedLocation = (locationId: string): boolean =>
    selectedLocationId === locationId

  $: getLocationRedirect = (locationId: string): string => `#` + locationId

  $: setCurrentLocation = (locationId: string): Promise<void> =>
    goto(getLocationRedirect(locationId))

  const createLayer = (locations: Location2[]) =>
    geoJson(createPointFeatures(locations), {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        const tooltipElement = createComponentAsDiv(LocationTooltip, { feature })
        layer.bindPopup(tooltipElement, { keepInView: true })
        layer.on("click", () => setCurrentLocation(feature.properties.id))
        layer.on("mouseover", () => layer.openPopup())
        layer.on("mouseout", () => layer.closePopup())
      },
    })

  onMount(() => {
    locationsPointLayer = createLayer(version.locations)
  })

  onDestroy(() => {
    if (map && locationsPointLayer) {
      map.removeLayer(locationsPointLayer)
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
          class:animate-fadeToWhite={isSelectedLocation(location.nid)}
          class:dark:animate-fadeToGray={isSelectedLocation(location.nid)}
        >
          <h3 class="heading4">
            <a
              href="#{location.nid}"
              on:click|preventDefault={() => setCurrentLocation(location.nid)}
            >
              {index + 1}. {$_("Location")}
              <small class="text-sm text-gray-500">
                #{location.nid}
              </small>
            </a>
          </h3>
          <DisplayField
            value={location.level_of_accuracy}
            fieldname="location.level_of_accuracy"
            showLabel
          />
          <DisplayField value={location.name} fieldname="location.name" showLabel />
          <DisplayField value={location.point} fieldname="location.point" showLabel />
          <DisplayField
            value={location.description}
            fieldname="location.description"
            showLabel
          />
          <DisplayField
            value={location.facility_name}
            fieldname="location.facility_name"
            showLabel
          />
          <DisplayField
            value={location.comment}
            fieldname="location.comment"
            showLabel
          />
          <LocationAreasField
            {map}
            label={$_("Areas")}
            areas={location.areas}
            locationId={location.nid}
            fieldname="location.areas"
            isSelectedEntry={isSelectedLocation(location.nid)}
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
