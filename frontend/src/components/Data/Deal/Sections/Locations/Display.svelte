<script lang="ts">
  import type { Point } from "geojson"
  import {
    Control,
    geoJson,
    icon,
    marker,
    type GeoJSON,
    type Layer,
    type Map,
  } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type {
    DealHull,
    Location2,
    PointFeature,
    PointFeatureProps,
  } from "$lib/types/newtypes"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"
  import { createPointFeatures, fitBounds } from "$lib/utils/location"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasField from "./LocationAreasField.svelte"
  import LocationLegend from "./LocationLegend.svelte"
  import LocationTooltip from "./LocationTooltip.svelte"

  export let deal: DealHull

  let map: Map | undefined
  let locationsPointLayer: GeoJSON<PointFeatureProps, Point>

  let selectedEntryId: string | undefined

  const onMapReady = (e: CustomEvent<Map>) => {
    map = e.detail

    const legend = new Control({ position: "bottomleft" })
    legend.onAdd = () => createComponentAsDiv(LocationLegend)
    map.addControl(legend)

    map.addLayer(locationsPointLayer)
    fitBounds(locationsPointLayer, map)
  }

  $: isAnyLocationSelected = (): boolean => selectedEntryId !== undefined

  $: isSelectedLocation = (locationId: string): boolean =>
    selectedEntryId === locationId

  $: getLocationRedirect = (locationId: string): string => `#` + locationId

  $: setCurrentLocation = (locationId: string): Promise<void> =>
    goto(getLocationRedirect(locationId))

  $: if (map && locationsPointLayer) {
    map.removeLayer(locationsPointLayer)
    locationsPointLayer = createLayer(deal.selected_version.locations)
    map.addLayer(locationsPointLayer)

    fitBounds(locationsPointLayer, map)
  }

  $: createLayer = (locations: Location2[]) =>
    geoJson(createPointFeatures(locations), {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        const tooltipElement = createComponentAsDiv(LocationTooltip, { feature })
        layer.bindPopup(tooltipElement, { keepInView: true })
        layer.on("click", () => setCurrentLocation(feature.properties.id))
        layer.on("mouseover", () => layer.openPopup())
        layer.on("mouseout", () => layer.closePopup())
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
    locationsPointLayer = createLayer(deal.selected_version.locations)
  })

  onDestroy(() => {
    if (map && locationsPointLayer) {
      map.removeLayer(locationsPointLayer)
    }
  })
</script>

<section class="flex flex-wrap lg:h-full">
  <div class="w-full overflow-y-auto p-2 lg:h-full lg:w-2/5">
    <SubmodelDisplayField
      entries={deal.selected_version.locations}
      bind:selectedEntryId
      label={$_("Location")}
      let:entry={location}
    >
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
      <DisplayField value={location.comment} fieldname="location.comment" showLabel />
      <LocationAreasField
        {map}
        label={$_("Areas")}
        areas={location.areas}
        fieldname="location.areas"
        isSelectedEntry={isSelectedLocation(location.nid)}
      />
    </SubmodelDisplayField>
  </div>
  <div class="h-[600px] w-full p-2 lg:w-3/5">
    <BigMap
      containerClass="min-h-full h-full"
      on:ready={onMapReady}
      options={{ center: [0, 0] }}
    />
  </div>
</section>
