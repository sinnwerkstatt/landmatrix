import { area } from "@turf/turf"
import type { Feature, FeatureCollection, Geometry, Point } from "geojson"
import * as L from "leaflet" // TODO: this breaks SSR
import type { GeoJSONOptions, LatLngBounds, LatLngLiteral, PathOptions } from "leaflet"
import * as R from "ramda"

import type {
  AreaFeature,
  AreaType,
  EnhancedAreaFeature,
  FeatureProps,
  Location,
  LocationWithCoordinates,
  PointFeature,
} from "$lib/types/deal"
import {
  addTempIds,
  createFeatureCollection,
  isPoint,
  setProperty,
  upsertProperties,
} from "$lib/utils/geojsonHelpers"

import LocationLegend from "$components/Deal/LocationLegend.svelte"
import LocationTooltip from "$components/Deal/LocationTooltip.svelte"

export const AREA_TYPES = ["production_area", "contract_area", "intended_area"] as const
export const AREA_TYPE_COLOR_MAP: { [key in AreaType]: string } = {
  contract_area: "#ff00ff",
  intended_area: "#66ff33",
  production_area: "#ff0000",
}

export const padBounds = (bounds: LatLngBounds): LatLngBounds => {
  const ne = bounds.getNorthEast()
  const sw = bounds.getSouthWest()

  if (ne.equals(sw)) {
    const margin = 0.2

    return L.latLngBounds(
      { lat: ne.lat + margin, lng: ne.lng + margin } as LatLngLiteral,
      { lat: sw.lat - margin, lng: sw.lng - margin } as LatLngLiteral,
    )
  }

  return bounds.pad(0.8)
}

// legacy check: new deals should always have coordinates
export const isLocationWithCoordinates = (
  location: Location,
): location is LocationWithCoordinates =>
  !!(
    location.point &&
    location.point.lat &&
    location.point.lng &&
    location.level_of_accuracy
  )

export const createPointFeature = (
  location: LocationWithCoordinates,
): Feature<Point, FeatureProps> => ({
  type: "Feature",
  geometry: {
    type: "Point",
    coordinates: [location.point.lng, location.point.lat],
  },
  properties: {
    id: location.id,
    level_of_accuracy: location.level_of_accuracy,
    name: location.name,
  },
})

export const addTempProperties: (features: Feature) => AreaFeature = R.converge(
  upsertProperties,
  [
    R.applySpec({ visible: R.pipe(R.path(["properties", "current"]), Boolean), area }),
    R.identity,
  ],
)

export const createEnhancedAreasCopy: (
  areas: FeatureCollection | undefined,
) => FeatureCollection = R.pipe(
  R.defaultTo(createFeatureCollection([])),
  R.prop("features"),
  R.map(addTempProperties),
  addTempIds,
  createFeatureCollection,
)

export const createEnhancedLocationsCopy: (locations: Location[]) => Location[] = R.map(
  R.evolve({ areas: createEnhancedAreasCopy }),
)

const getPointFeatures: (locations: Location[]) => PointFeature[] = R.pipe<
  [Location[]],
  LocationWithCoordinates[],
  PointFeature[]
>(R.filter(isLocationWithCoordinates), R.map(createPointFeature))

const getAreaFeatures: (locations: Location[]) => EnhancedAreaFeature[] = R.pipe(
  R.map(
    R.pipe(
      R.path<EnhancedAreaFeature[]>(["areas", "features"]),
      R.defaultTo([] as EnhancedAreaFeature[]),
    ),
  ),
  R.flatten,
)

export const createLocationFeatures: (
  locations: Location[],
) => (PointFeature | EnhancedAreaFeature)[] = R.converge(
  R.concat as <T>(a1: T[], a2: T[]) => T[],
  [getPointFeatures, getAreaFeatures],
)

export const toggleFeatureVisibility = (
  featureId: string,
): ((location: Location) => Location) =>
  R.evolve({
    areas: (areas: FeatureCollection): FeatureCollection => {
      const features = areas.features as EnhancedAreaFeature[]
      const featureIndex = features?.findIndex(f => f.id === featureId)
      const updatedFeatures = R.adjust(
        featureIndex,
        f => setProperty("visible", !f.properties.visible, f),
        features,
      )
      return createFeatureCollection(updatedFeatures)
    },
  })

export const createTooltip = (
  feature: Feature<Geometry, FeatureProps>,
): HTMLElement => {
  const container = L.DomUtil.create("div")
  new LocationTooltip({
    props: { feature },
    target: container,
  })
  return container
}

export const createLegend = () => {
  const legend = new L.Control({ position: "bottomleft" })
  legend.onAdd = () => {
    const container = L.DomUtil.create("div")
    new LocationLegend({
      props: {},
      target: container,
    })
    return container
  }
  return legend
}

export const createGeoJsonOptions = ({
  getCurrentLocation,
  setCurrentLocation,
}: {
  getCurrentLocation: () => string | undefined
  setCurrentLocation: (locationId: string) => void
}): GeoJSONOptions => ({
  // area styles
  style: feature => {
    const castedFeature = feature as EnhancedAreaFeature
    const currentLocation = getCurrentLocation()

    return {
      weight: 1.5,
      color: "#000000",
      opacity: castedFeature.properties.visible ? 1 : 0,
      fillOpacity: castedFeature.properties.visible ? 0.4 : 0,
      className:
        !currentLocation || castedFeature.properties.id === currentLocation
          ? ""
          : "leaflet-hidden",
      dashArray: "5, 5",
      dashOffset: "0",
      fillColor: AREA_TYPE_COLOR_MAP[castedFeature?.properties.type],
    } as PathOptions
  },
  // point styles
  pointToLayer: (feature: PointFeature, latlng) => {
    const currentLocation = getCurrentLocation()
    return L.marker(latlng, {
      icon: L.icon({
        iconUrl: "/images/marker-icon.png",
        shadowUrl: "/images/marker-shadow.png",
        // shadowSize: [0, 0],
        iconAnchor: [12.5, 41],
        popupAnchor: [0, -35],
        className:
          !currentLocation || currentLocation === feature.properties.id
            ? ""
            : "leaflet-hidden",
      }),
    })
  },
  // layer controls
  onEachFeature: (feature: PointFeature | EnhancedAreaFeature, layer) => {
    if (isPoint(feature)) {
      layer.bindPopup(createTooltip(feature), {
        keepInView: true,
      })
      layer.on("click", () =>
        setCurrentLocation(
          feature.properties.id === getCurrentLocation() ? "" : feature.properties.id,
        ),
      )
      layer.on("mouseover", () => layer.openPopup())
      layer.on("mouseout", () => layer.closePopup())
    }
  },
  // filter: (geoJsonFeature: PointFeature | EnhancedAreaFeature) => {
  //   if (isPoint(geoJsonFeature)) {
  //     return true
  //   }
  //   const currentLocation = getCurrentLocation()
  //   return currentLocation ? geoJsonFeature.properties.id === currentLocation : true
  // },
})
