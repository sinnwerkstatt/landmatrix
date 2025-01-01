<script lang="ts">
  import { Feature, type Map } from "ol"
  import { Point } from "ol/geom"
  import { Vector as VectorLayer } from "ol/layer"
  import { fromLonLat } from "ol/proj"
  import { Vector as VectorSource } from "ol/source"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/state"

  import { filters } from "$lib/filters"
  import type { Marker as MarkerType } from "$lib/types/wagtail"

  import OLMap from "$components/Map/OLMap.svelte"

  import { markerStyle, olStyle2 } from "./mapHelper"

  interface Props {
    countryID?: number
    regionID?: number
    markers?: MarkerType[]
  }

  let { countryID, regionID, markers = [] }: Props = $props()

  let map: Map | undefined = $state()
  const markersVectorSource = new VectorSource({})

  function _drawGlobalMarkers() {
    for (let mark of markers) {
      // console.log(mark)
      const feature = new Feature({
        geometry: new Point(fromLonLat([mark.coordinates[1], mark.coordinates[0]])),
        regionId: mark.region_id,
      })
      const country_name = page.data.regions.find(r => r.id === mark.region_id)!.name
      // styleCircle(circle, mark.count! / 50, country_name, true, 30)
      feature.setStyle(olStyle2(mark.count! / 50, country_name))
      markersVectorSource.addFeature(feature)
    }
  }

  function _drawRegionMarkers() {
    for (let mark of markers) {
      const feature = new Feature({
        geometry: new Point(fromLonLat([mark.coordinates[1], mark.coordinates[0]])),
        countryId: mark.country_id,
      })

      const radius = mark.count! / 10
      feature.setStyle(olStyle2(radius, mark.count?.toString()))

      markersVectorSource.addFeature(feature)
    }
  }

  function _drawCountryMarkers() {
    for (let mark of markers)
      markersVectorSource.addFeature(
        new Feature({
          geometry: new Point(fromLonLat([mark.coordinates[1], mark.coordinates[0]])),
        }),
      )
  }

  const onClickMap = async () => {
    if (regionID) {
      $filters.region_id = regionID
      $filters.country_id = undefined
    } else if (countryID) {
      $filters.region_id = undefined
      $filters.country_id = countryID
    }
  }

  const drawMarkers = () => {
    if (!map || !markers || !browser) return

    if (regionID) _drawRegionMarkers()
    else if (countryID) _drawCountryMarkers()
    else _drawGlobalMarkers()
  }

  const onMapReady = (_map: Map) => {
    map = _map

    map.addLayer(
      new VectorLayer({
        source: markersVectorSource,
        style: () => markerStyle,
      }),
    )

    let extent: number[] | undefined
    if (regionID) {
      const reg = page.data.regions.find(r => r.id === regionID)!
      extent = [
        ...fromLonLat([reg.point_lon_min, reg.point_lat_min]),
        ...fromLonLat([reg.point_lon_max, reg.point_lat_max]),
      ]
    } else if (countryID) {
      const country = page.data.countries.find(c => c.id === countryID)!
      extent = [
        ...fromLonLat([country.point_lon_min, country.point_lat_min]),
        ...fromLonLat([country.point_lon_max, country.point_lat_max]),
      ]
    } else {
      const mapView = map.getView()
      mapView.setCenter(fromLonLat([12, 30]))
      mapView.setZoom(0)
    }

    if (extent) map.getView().fit(extent, { padding: [30, 30, 30, 30] })

    drawMarkers()
  }
</script>

<div
  class="relative mt-6 h-[30vh] min-h-[300px] w-full cursor-pointer border border-orange shadow-md hover:border-orange-300"
>
  <a
    class="group absolute z-20 flex h-full w-full bg-transparent transition duration-300 hover:bg-orange/20"
    href="/map/"
    onclick={onClickMap}
  >
    <span
      class="z-1 hover-text invisible w-full self-center text-center text-[4rem] font-bold text-white opacity-0 transition duration-500 group-hover:visible group-hover:opacity-100"
    >
      {$_("Go to map")}
    </span>
  </a>
  <OLMap
    containerClass="min-h-full h-full"
    mapReady={onMapReady}
    options={{ zoomControl: false, center: [12, 30] }}
  />
</div>
