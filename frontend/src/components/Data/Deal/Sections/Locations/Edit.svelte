<script lang="ts">
  import { Feature, MapBrowserEvent, type Map } from "ol"
  import { Control } from "ol/control"
  import { GeoJSON } from "ol/format"
  import { Point } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { fromLonLat } from "ol/proj"
  import { Vector as VectorSource } from "ol/source"
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import { type DealHull, type Location2, type Mutable } from "$lib/types/data"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"
  import LocationDot from "$components/icons/LocationDot.svelte"
  import { markerStyle, markerStyleSemi } from "$components/Map/mapHelper"
  import OLMap from "$components/Map/OLMap.svelte"

  import Entry from "./Entry.svelte"
  import LocationLegend from "./LocationLegend.svelte"
  import {
    createLocation,
    createLocationTooltipOverlay,
    isEmptyLocation,
  } from "./locations"

  interface Props {
    deal: Mutable<DealHull>
  }

  let { deal = $bindable() }: Props = $props()

  let locations = $state(deal.selected_version.locations)
  let country = $state(page.data.countries.find(c => c.id === deal.country_id))

  let selectedEntryId: string | undefined = $state()
  let editPointMode = $state(false)
  let map: Map | undefined = $state()

  let markersVectorSource = new VectorSource({})
  let addingMarkerVectorSource = new VectorSource({})

  const createMarkerLayer = (locations: readonly Location2[]) => {
    markersVectorSource.clear()
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

  $effect(() => {
    createMarkerLayer(locations)
  })

  const onMapReady = (_map: Map) => {
    map = _map

    map.addControl(
      new Control({
        element: createComponentAsDiv(LocationLegend, { rightCorner: true }),
      }),
    )

    map.addLayer(
      new VectorLayer({ source: markersVectorSource, style: () => markerStyle }),
    )
    map.addLayer(
      new VectorLayer({ source: addingMarkerVectorSource, style: () => markerStyle }),
    )

    map.on("pointermove", evt => {
      const feature = map!.forEachFeatureAtPixel(evt.pixel, function (feature) {
        return feature as Feature<Point>
      })

      if (feature && markersVectorSource.hasFeature(feature)) {
        createLocationTooltipOverlay(feature).then(ovrl => {
          map!.addOverlay(ovrl)
          map!.getOverlays().forEach(overlay => {
            if (overlay !== ovrl) map!.removeOverlay(overlay)
          })
        })
      } else {
        map!.getOverlays().forEach(overlay => map!.removeOverlay(overlay))
      }
    })
    map.on("click", evt => {
      const feature = map!.forEachFeatureAtPixel(evt.pixel, function (feature) {
        return feature as Feature<Point>
      })

      if (feature && markersVectorSource.hasFeature(feature)) {
        const locationId = feature.getProperties().nid
        const locrec = `#` + (selectedEntryId === locationId ? "" : locationId)
        goto(locrec)
      }
    })
  }

  $effect(() => {
    if (!map) return
    const mapView = map.getView()

    if (markersVectorSource.getFeatures().length > 0) {
      mapView.fit(markersVectorSource.getExtent(), {
        padding: [150, 150, 150, 150],
        maxZoom: 13,
      })
    } else if (country) {
      mapView.fit(
        [
          ...fromLonLat([country.point_lon_min, country.point_lat_min]),
          ...fromLonLat([country.point_lon_max, country.point_lat_max]),
        ],
        { padding: [30, 30, 30, 30] },
      )
    }
  })

  // Point adding/moving logic
  let addingPointPoint: Point | undefined = $state()
  let addingPointFeature: Feature | undefined = $state()
  const postAddingPointcleanup = () => {
    if (!map) return
    addingMarkerVectorSource.clear()
    addingPointFeature = undefined
    addingPointPoint = undefined
    map.un("click", onClickOnMapEvent)
  }
  const onClickOnMapEvent = (e: MapBrowserEvent<UIEvent>) => {
    const pt = new Point(e.coordinate)
    const ft = new Feature<Point>({ geometry: pt })
    addingMarkerVectorSource.addFeature(ft)
    const ptGeoJSON = new GeoJSON({
      dataProjection: "EPSG:4326",
      featureProjection: "EPSG:3857",
    }).writeGeometryObject(pt, { decimals: 6 })
    const selectedEntryIndex = locations.findIndex(l => l.nid === selectedEntryId)
    locations[selectedEntryIndex].point = ptGeoJSON
    syncChangesUpstream()
    postAddingPointcleanup()
    editPointMode = false
  }
  const toggleMarkerMode = () => {
    if (!map) return
    editPointMode = !editPointMode
    if (editPointMode) {
      const _extent = map.getView().calculateExtent(map.getSize())
      addingPointPoint = new Point([_extent[0], _extent[1]])
      addingPointFeature = new Feature({
        geometry: addingPointPoint,
      })
      addingPointFeature.setStyle(markerStyleSemi)
      addingMarkerVectorSource.addFeature(addingPointFeature)
      map.on("pointermove", e => addingPointPoint?.setCoordinates(e.coordinate))
      map.on("click", onClickOnMapEvent)
    } else {
      postAddingPointcleanup()
    }
  }

  const syncChangesUpstream = () => {
    deal.selected_version.locations = locations
  }
</script>

{JSON.stringify(deal.selected_version.locations)}
<form class="grid h-full gap-2 lg:grid-cols-5" id="locations">
  <div class="lg:order-last lg:col-span-3">
    <OLMap
      containerClass="h-full min-h-[300px]"
      mapReady={onMapReady}
      showLayerSwitcher
    >
      {#if selectedEntryId && locations.find(l => l.nid === selectedEntryId)}
        <div
          class={twMerge(
            "absolute bottom-3 left-3 z-10",
            editPointMode ? "bg-orange text-white" : "bg-white text-orange",
          )}
        >
          <button
            type="button"
            class="z-10 h-[40px] w-[40px] rounded border-2 border-black/30 px-2 pb-1.5 pt-0.5"
            onclick={toggleMarkerMode}
            title={$_("Create or move point")}
          >
            <LocationDot class="inline size-5" />
          </button>
        </div>
      {/if}
    </OLMap>
  </div>

  <div class="h-full lg:col-span-2 lg:overflow-y-auto">
    <SubmodelEditField
      bind:entries={locations}
      bind:selectedEntryId
      createEntry={createLocation}
      entryComponent={Entry}
      extras={{ map, country }}
      isEmpty={isEmptyLocation}
      label={$_("Location")}
      onchange={syncChangesUpstream}
    />
  </div>
</form>
