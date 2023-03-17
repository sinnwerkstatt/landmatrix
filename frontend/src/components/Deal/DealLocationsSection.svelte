<script lang="ts">
  import type {
    Map,
    GeoJSONOptions,
    GeoJSON,
    StyleFunction,
    PathOptions,
    LatLngBoundsExpression,
  } from "leaflet"
  import { latLngBounds, geoJson, DomUtil } from "leaflet?client"
  import type { Feature, Geometry } from "geojson"

  import type { Deal, AreaType } from "$lib/types/deal"

  import BigMap from "$components/Map/BigMap.svelte"
  import LocationTooltip from "$components/Deal/LocationTooltip.svelte"

  import DealSubmodelSection from "./DealSubmodelSection.svelte"

  export let deal: Deal

  interface FeatureProperties {
    id: string
    name: string
    type: AreaType
    year: number
  }

  let bigmap: Map
  let geoJsonLayer: GeoJSON<FeatureProperties>

  const styleFunction: StyleFunction<FeatureProperties> = feature => {
    const commonStyles: PathOptions = {
      weight: 2,
      color: "#000000",
      opacity: 1,
      fillOpacity: 0.2,
    }
    const areaTypeStylesMap: { [key in AreaType]: PathOptions } = {
      contract_area: { dashArray: "5, 5", dashOffset: "0", fillColor: "#ff00ff" },
      intended_area: { dashArray: "5, 5", dashOffset: "0", fillColor: "#66ff33" },
      production_area: { fillColor: "#ff0000" },
    }
    return {
      ...commonStyles,
      ...areaTypeStylesMap[feature?.properties.type],
    }
  }

  const createTooltip = (
    feature: Feature<Geometry, FeatureProperties>,
  ): HTMLElement => {
    const container = DomUtil.create("div")
    new LocationTooltip({
      props: { feature },
      target: container,
    })
    return container
  }

  const geoJsonOptions: GeoJSONOptions<FeatureProperties> = {
    style: styleFunction,
    onEachFeature: (feature, layer) => {
      const tooltip = createTooltip(feature)

      layer.bindPopup(tooltip, { permanent: false, sticky: true, keepInView: true })
      layer.on("mouseover", () => layer.openPopup())
      layer.on("mouseout", () => layer.closePopup())
    },
  }

  const computeBounds = (geoJsonLayer: GeoJSON): LatLngBoundsExpression => {
    const bounds = geoJsonLayer.getBounds()

    let ne = bounds.getNorthEast()
    let sw = bounds.getSouthWest()
    if (ne && sw) {
      if (ne.equals(sw)) {
        ne.lat += 10
        ne.lng += 10
        sw.lat -= 10
        sw.lng -= 10
        return latLngBounds(ne, sw)
      }
      return bounds.pad(1.2)
    }
    return
  }

  const refreshMap = async (): Promise<void> => {
    if (!(deal && deal.country && bigmap)) {
      return
    }

    if (geoJsonLayer) {
      bigmap.removeLayer(geoJsonLayer)
    }
    geoJsonLayer = geoJson(deal.geojson, geoJsonOptions)
    bigmap.addLayer(geoJsonLayer)

    const bounds = computeBounds(geoJsonLayer)
    if (bounds) {
      bigmap.fitBounds(bounds, { animate: false })
    }
  }

  const onMapReady = async (event: CustomEvent<Map>) => {
    bigmap = event.detail
    await refreshMap()
  }
</script>

<DealSubmodelSection model="location" modelName="Location" entries={deal.locations}>
  <div class="min-h-[20rem] w-full lg:w-1/2">
    <BigMap
      containerClass="min-h-full h-full mt-5"
      options={{ center: [0, 0] }}
      on:ready={onMapReady}
    />
  </div>
</DealSubmodelSection>
