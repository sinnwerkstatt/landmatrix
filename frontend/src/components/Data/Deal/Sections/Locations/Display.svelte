<script lang="ts">
  import { Feature, type Map } from "ol"
  import { Control } from "ol/control"
  import { Point } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { fromLonLat } from "ol/proj"
  import { Vector as VectorSource } from "ol/source"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import type { components } from "$lib/openAPI"
  import type { DealHull, Location } from "$lib/types/data"
  import { createComponentAsDiv } from "$lib/utils/domHelpers"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"
  import { markerStyle, markerStyleSemi } from "$components/Map/mapHelper"
  import { fitMapToFeatures } from "$components/Map/mapstuff.svelte"
  import OLMap from "$components/Map/OLMap.svelte"

  import LocationAreasField from "./LocationAreasField.svelte"
  import LocationLegend from "./LocationLegend.svelte"
  import { createLocationTooltipOverlay } from "./locations"

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
          createLocationTooltipOverlay(ft as Feature<Point>).then(ovrl => {
            map!.addOverlay(ovrl)
            map!.getOverlays().forEach(overlay => {
              if (overlay !== ovrl) map!.removeOverlay(overlay)
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
      const feature = map!.forEachFeatureAtPixel(
        evt.pixel,
        feature => feature as Feature<Point>,
      )

      hoverLocationId =
        feature && markersVectorSource.hasFeature(feature)
          ? feature.getProperties().nid
          : undefined
    })
    map.on("click", evt => {
      const feature = map!.forEachFeatureAtPixel(
        evt.pixel,
        feature => feature as Feature<Point>,
      )
      if (feature && markersVectorSource.hasFeature(feature)) {
        const nid = feature.getProperties().nid
        goto(nid === selectedLocationId ? "" : `#${nid}`)
      }
    })
  }

  const createMarkerLayer = (locations: readonly Location[]) => {
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

  $effect(() => {
    if (!map) return

    if (deal.selected_version.locations.length) {
      fitMapToFeatures(map)
    } else {
      const cntry = page.data.countries.find(x => x.id === deal.country_id)
      if (!cntry) return
      map
        .getView()
        .fit(
          [
            ...fromLonLat([cntry.point_lon_min, cntry.point_lat_min]),
            ...fromLonLat([cntry.point_lon_max, cntry.point_lat_max]),
          ],
          { padding: [30, 30, 30, 30] },
        )
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
      model="deal"
      fieldname="locations"
      label={$_("Location")}
      entries={deal.selected_version.locations}
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
        {#if map}
          <LocationAreasField
            {map}
            label={$_("Areas")}
            areas={location.areas}
            fieldname="location.areas"
            isSelectedEntry={!selectedLocationId || location.nid === selectedLocationId}
          />
        {/if}
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
