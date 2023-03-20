<script lang="ts">
  import type {
    Map,
    GeoJSONOptions,
    GeoJSON,
    StyleFunction,
    PathOptions,
    Marker,
  } from "leaflet"
  import { geoJson, DomUtil, Polygon } from "leaflet?client"
  import type { Feature, Geometry } from "geojson"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import type { Deal, AreaType, Location, FeatureProps } from "$lib/types/deal"

  import BigMap from "$components/Map/BigMap.svelte"
  import LocationTooltip from "$components/Deal/LocationTooltip.svelte"
  import {
    isLocationWithCoordinates,
    padBounds,
    createPointFeature,
  } from "$components/Deal/Location/location.js"
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection.svelte"
  import { isPoint } from "$components/Deal/Location/geojson"

  export let deal: Deal

  let bigmap: Map
  let geoJsonLayer: GeoJSON<FeatureProps>
  $: pointFeatures = deal.locations
    .filter(isLocationWithCoordinates)
    .map(createPointFeature)
    .map(feature => ({
      ...feature,
      properties: {
        ...feature.properties,
        visible: true,
      },
    }))

  $: areaFeatures = deal.locations
    .reduce(
      (acc: Feature<Polygon, FeatureProps>[], val: Location) => [
        ...acc,
        ...(val.areas?.features ?? []),
      ],
      [],
    )
    .map(feature => ({
      ...feature,
      properties: {
        ...feature.properties,
        visible: !!feature.properties?.current,
      },
    }))

  const styleFunction: StyleFunction<FeatureProps> = feature => {
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

  const createTooltip = (feature: Feature<Geometry, FeatureProps>): HTMLElement => {
    const container = DomUtil.create("div")
    new LocationTooltip({
      props: { feature },
      target: container,
    })
    return container
  }
  const geoJsonOptions: GeoJSONOptions<FeatureProps> = {
    style: styleFunction,
    onEachFeature: (feature, layer) => {
      if (isPoint(feature)) {
        layer.bindPopup(createTooltip(feature), {
          permanent: false,
          sticky: true,
          keepInView: true,
        })
      }
      layer.on("mouseover", () => layer.openPopup())
      layer.on("mouseout", () => layer.closePopup())
      layer.on("click", () => setCurrentLocation(feature.properties.id))
    },
  }

  const onToggleVisibility = e => {
    const { index, location } = e.detail

    const toggleVisibility = (feature: Feature): Feature => ({
      ...feature,
      properties: {
        ...feature.properties,
        visible: !feature.properties?.visible,
      },
    })
    const locationFeatures = areaFeatures
      .filter(f => f.properties.id === location)
      .map((f, i) => (i === index ? toggleVisibility(f) : f))
    const otherFeatures = areaFeatures.filter(f => f.properties.id !== location)
    areaFeatures = [...locationFeatures, ...otherFeatures]
  }

  const refreshMap = (): void => {
    if (!(deal && deal.country && bigmap)) {
      return
    }

    if (geoJsonLayer) {
      bigmap.removeLayer(geoJsonLayer)
    }

    geoJsonLayer = geoJson([...pointFeatures, ...areaFeatures], geoJsonOptions)

    bigmap.addLayer(geoJsonLayer)

    geoJsonLayer.eachLayer((layer: Marker<FeatureProps> | Polygon<FeatureProps>) => {
      const element = layer.getElement()
      const feature = layer.feature

      if (feature?.properties.id === currentLocation && feature?.properties.visible) {
        element?.classList.remove("leaflet-hidden")
      } else {
        element?.classList.add("leaflet-hidden")
      }
    })

    const bounds = geoJsonLayer.getBounds()
    if (bounds.isValid()) {
      bigmap.fitBounds(padBounds(bounds), { animate: false })
    }
  }

  const onMapReady = (event: CustomEvent<Map>) => {
    bigmap = event.detail
    refreshMap()
  }

  let currentLocation: string | undefined
  $: currentLocation = $page.url.hash.split("/")?.[1]

  const setCurrentLocation = (id: string) => {
    currentLocation = id
  }

  $: if (bigmap && geoJsonLayer && currentLocation) {
    refreshMap()
  }
  $: if (bigmap && geoJsonLayer && areaFeatures) {
    refreshMap()
  }
</script>

{#if browser}
  <section class="flex">
    <div class="max-h-[75vh] w-full overflow-y-auto p-2 lg:w-1/2">
      <DealSubmodelSection
        bind:selectedEntryId={currentLocation}
        model="location"
        modelName="Location"
        entries={deal.locations}
        on:toggleVisibility={onToggleVisibility}
      />
    </div>
    <div class="min-h-[20rem] w-full p-2 lg:w-1/2">
      <BigMap
        containerClass="min-h-full h-full"
        options={{ center: [0, 0] }}
        on:ready={onMapReady}
      />
    </div>
  </section>
{/if}

<style>
  :global(path.leaflet-hidden) {
    /*display: none;*/
    opacity: 0.3;
    filter: saturate(0);
  }

  :global(img.leaflet-hidden) {
    /*opacity: 0.6;*/
    filter: saturate(0);
  }
</style>
