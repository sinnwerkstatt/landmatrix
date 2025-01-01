<script lang="ts">
  import { Feature, Overlay, type Map } from "ol"
  import { Control } from "ol/control"
  import { Point } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { fromLonLat } from "ol/proj"
  import { Vector as VectorSource } from "ol/source"
  import { mount, onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import type { components } from "$lib/openAPI"
  import type { DealHull, Location2 } from "$lib/types/data"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"

  import LocationTooltip from "$components/Data/Deal/Sections/Locations/LocationTooltip.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"
  import { markerStyle, markerStyleSemi } from "$components/Map/mapHelper"
  import OLMap from "$components/Map/OLMap.svelte"
  import { createCoordinatesMap } from "$components/Map/utils"

  import LocationAreasField from "./LocationAreasField.svelte"
  import LocationLegend from "./LocationLegend.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()

  let map: Map | undefined = $state()
  let markersVectorSource = new VectorSource({})

  let selectedLocationId: string | undefined = $state()
  let hoverLocationId: string | undefined = $state()

  const updateHoverState = async (hoverLocationId?: string) => {
    if (!map) return
    let haveHit = false
    if (hoverLocationId)
      markersVectorSource.forEachFeature(ft => {
        const prps = ft.getProperties()
        if (prps.nid === hoverLocationId) {
          haveHit = true
          createMarkerPopup(ft as Feature<Point>).then(newOverlay => {
            map!.getOverlays().forEach(overlay => {
              if (overlay !== newOverlay) map!.removeOverlay(overlay)
            })
          })
        }
      })
    if (!haveHit) {
      map!.getOverlays().forEach(overlay => map!.removeOverlay(overlay))
    }
  }

  const updateSelectState = (selectedLocationId?: string) => {
    if (!map) return
    let haveHit = false
    if (selectedLocationId)
      markersVectorSource.forEachFeature(ft => {
        const prps = ft.getProperties()
        if (prps.nid === selectedLocationId) {
          haveHit = true
          ft.setStyle(markerStyle)
        } else {
          ft.setStyle(markerStyleSemi)
        }
      })
    if (!haveHit) {
      markersVectorSource.forEachFeature(ft => ft.setStyle(markerStyle))
    }
  }

  const onMapReady = (_map: Map) => {
    map = _map

    map.addControl(new Control({ element: createComponentAsDiv(LocationLegend) }))

    map.addLayer(
      new VectorLayer({ source: markersVectorSource, style: () => markerStyle }),
    )

    map.on("pointermove", evt => {
      const feature = map!.forEachFeatureAtPixel(evt.pixel, function (feature) {
        return feature as Feature<Point>
      })
      hoverLocationId = feature?.getProperties()?.nid
    })
    map.on("click", evt => {
      const feature = map!.forEachFeatureAtPixel(evt.pixel, function (feature) {
        return feature as Feature<Point>
      })
      if (feature) {
        const nid = feature.getProperties().nid
        goto(nid === selectedLocationId ? "" : `#${nid}`)
      }
    })
  }

  async function createMarkerPopup(feature: Feature<Point>) {
    const markerContainerDiv = document.createElement("div")

    mount(LocationTooltip, { target: markerContainerDiv, props: { feature } })

    const ovrlay = new Overlay({
      element: markerContainerDiv,
      position: feature.getGeometry()?.getCoordinates(),
      positioning: "bottom-center",
      offset: [-30, -30, -30, -30],
      autoPan: { animation: { duration: 300 } },
    })
    map!.addOverlay(ovrlay)
    return ovrlay
  }

  const createMarkerLayer = (locations: readonly Location2[]) => {
    const points = []
    for (const location of locations) {
      if (location.point) {
        const feature = new Feature<Point>({
          geometry: new Point(fromLonLat(location.point.coordinates!)),
        })

        feature.setProperties({
          nid: location.nid,
          level_of_accuracy: location.level_of_accuracy,
          name: location.name,
          point: location.point.coordinates,
        })

        points.push(feature)
      }
    }
    markersVectorSource.addFeatures(points)
  }

  onMount(() => createMarkerLayer(deal.selected_version.locations))
  onDestroy(() => markersVectorSource.clear())

  let countryCoords = $derived(createCoordinatesMap(page.data.countries))
  $effect(() => {
    if (!map) return
    const mapView = map.getView()
    // map.removeLayer(markerFeatureGroup)
    // markerFeatureGroup = createMarkerLayer(deal.selected_version.locations)
    // map.addLayer(markerFeatureGroup)

    if (!deal.selected_version.locations.length) {
      const coords = countryCoords[deal.country_id!]
      mapView.fit(fromLonLat(coords), { padding: [30, 30, 30, 30] })
    } else {
      mapView.fit(markersVectorSource.getExtent(), {
        padding: [150, 150, 150, 150],
        maxZoom: 13,
      })
    }
  })

  $effect(() => {
    updateHoverState(hoverLocationId)
  })
  $effect(() => {
    updateSelectState(selectedLocationId)
  })
</script>

<section class="flex flex-wrap lg:h-full">
  <div class="w-full overflow-y-auto p-2 lg:h-full lg:w-2/5">
    <SubmodelDisplayField
      bind:hoverEntryId={hoverLocationId}
      bind:selectedEntryId={selectedLocationId}
      entries={deal.selected_version.locations}
      label={$_("Location")}
    >
      {#snippet children(location: components["schemas"]["Location"])}
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
      {/snippet}
    </SubmodelDisplayField>
  </div>
  <div class="sticky top-0 h-[600px] w-full p-2 lg:w-3/5">
    <OLMap
      containerClass="min-h-full h-full"
      mapReady={onMapReady}
      options={{ center: [0, 0] }}
      showLayerSwitcher
    />
  </div>
</section>
