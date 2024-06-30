<script lang="ts">
  import type { Point } from "geojson"
  import type { GeoJSON, Layer, Map, Marker } from "leaflet?client"
  import { Control, geoJson } from "leaflet?client"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type {
    DealHull,
    Location2,
    PointFeature,
    PointFeatureProps,
  } from "$lib/types/data"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"
  import BigMap from "$components/Map/BigMap.svelte"

  import LocationAreasField from "./LocationAreasField.svelte"
  import LocationLegend from "./LocationLegend.svelte"
  import { createPointFeatures, fitBounds } from "./locations"
  import LocationTooltip from "./LocationTooltip.svelte"

  export let deal: DealHull

  let map: Map | undefined
  let markerFeatureGroup: GeoJSON<PointFeatureProps, Point>

  let selectedLocationId: string | undefined
  let hoverLocationId: string | undefined

  $: if (map) {
    map.removeLayer(markerFeatureGroup)
    markerFeatureGroup = createMarkerLayer(deal.selected_version.locations)
    map.addLayer(markerFeatureGroup)

    fitBounds(map)
  }

  $: if (map) {
    markerFeatureGroup.eachLayer(updateHoverState(hoverLocationId))
  }

  $: if (map) {
    markerFeatureGroup.eachLayer(updateSelectState(selectedLocationId))
  }

  const updateHoverState = (hoverLocationId?: string) => (layer: Layer) => {
    const marker = layer as Marker
    const feature: PointFeature = marker.feature!

    if (feature.properties.id === hoverLocationId) {
      marker.openPopup()
    } else {
      marker.closePopup()
    }
  }

  const updateSelectState = (selectedLocationId?: string) => (layer: Layer) => {
    const marker = layer as Marker
    const feature: PointFeature = marker.feature!
    const isSelectedLocation = feature.properties.id === selectedLocationId

    marker.removeEventListener("mousedown")
    marker.on("mousedown", () =>
      isSelectedLocation ? goto("") : goto(`#${feature.properties.id}`),
    )

    // FIXME: use marker.setIcon(Icon) with newly styled Icon
    if (!selectedLocationId || isSelectedLocation) {
      marker._icon.classList.remove("leaflet-hidden")
    } else {
      marker._icon.classList.add("leaflet-hidden")
    }
  }

  const onMapReady = (e: CustomEvent<Map>) => {
    const _map = e.detail

    const legend = new Control({ position: "bottomleft" })
    legend.onAdd = () => createComponentAsDiv(LocationLegend)
    _map.addControl(legend)

    // set at the end to avoid svelte reactivity issues
    map = _map
  }

  const createMarkerLayer = (locations: readonly Location2[]) =>
    geoJson([...createPointFeatures(locations)], {
      onEachFeature: (feature: PointFeature, layer: Layer) => {
        const tooltipElement = createComponentAsDiv(LocationTooltip, { feature })
        layer.bindPopup(tooltipElement, {
          keepInView: true,
          autoPanPaddingTopLeft: [20, 20],
          autoPanPaddingBottomRight: [20, 100],
        })
        layer.on("mouseover", () => (hoverLocationId = feature.properties.id))
        layer.on("mouseout", () => (hoverLocationId = undefined))
      },
    })

  onMount(() => {
    markerFeatureGroup = createMarkerLayer(deal.selected_version.locations)
  })

  onDestroy(() => {
    if (map) {
      map.removeLayer(markerFeatureGroup)
    }
  })
</script>

<section class="flex flex-wrap lg:h-full">
  <div class="w-full overflow-y-auto p-2 lg:h-full lg:w-2/5">
    <SubmodelDisplayField
      entries={deal.selected_version.locations}
      bind:selectedEntryId={selectedLocationId}
      bind:hoverEntryId={hoverLocationId}
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
        isSelectedEntry={!selectedLocationId || location.nid === selectedLocationId}
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
