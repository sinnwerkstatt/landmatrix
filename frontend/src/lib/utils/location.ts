import type { Feature, Point, FeatureCollection, Geometry } from "geojson"
import * as L from "leaflet"
import * as R from "ramda"
import { area } from "@turf/turf"
import { marker, icon, Control } from "leaflet"

import type {
  AreaType,
  FeatureProps,
  Location,
  LocationWithCoordinates,
  AreaFeature,
  PointFeature,
  EnhancedAreaFeature,
} from "$lib/types/deal"
import {
  upsertProperties,
  createFeatureCollection,
  addTempIds,
  setProperty,
  isPoint,
} from "$lib/utils/geojsonHelpers"

import LocationTooltip from "$components/Deal/LocationTooltip.svelte"
import LocationLegend from "$components/Deal/LocationLegend.svelte"

export const AREA_TYPES = ["production_area", "contract_area", "intended_area"] as const
export const AREA_TYPE_COLOR_MAP: { [key in AreaType]: string } = {
  contract_area: "#ff00ff",
  intended_area: "#66ff33",
  production_area: "#ff0000",
}

export const padBounds = (bounds: L.LatLngBounds): L.LatLngBounds => {
  const ne = bounds.getNorthEast()
  const sw = bounds.getSouthWest()

  if (ne.equals(sw)) {
    const margin = 10

    return L.latLngBounds(
      L.latLng(ne.lat + margin, ne.lng + margin),
      L.latLng(sw.lat - margin, sw.lng - margin),
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
    R.applySpec({
      visible: R.pipe(R.path(["properties", "current"]), Boolean),
      area,
    }),
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
  R.evolve({
    areas: createEnhancedAreasCopy,
  }),
)

export const createLocationFeatures = (
  locations: Location[],
): (PointFeature | EnhancedAreaFeature)[] => {
  const pointFeatures: PointFeature[] = locations
    .filter(isLocationWithCoordinates)
    .map(createPointFeature)

  const areaFeatures: EnhancedAreaFeature[] = R.pipe<
    [Location[]],
    EnhancedAreaFeature[][],
    EnhancedAreaFeature[]
  >(
    R.map(
      R.path(["areas", "features"]) as (location: Location) => EnhancedAreaFeature[],
    ),
    R.flatten,
  )(locations)

  return [...pointFeatures, ...areaFeatures]
}

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
  const legend = new Control({ position: "bottomleft" })
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
}): L.GeoJSONOptions => ({
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
    } as L.PathOptions
  },
  // point styles
  pointToLayer: (feature: PointFeature, latlng) => {
    const currentLocation = getCurrentLocation()
    return marker(latlng, {
      icon: icon({
        iconRetinaUrl: "/images/marker-icon-2x.png",
        iconUrl: "/images/marker-icon.png",
        shadowUrl: "/images/marker-shadow.png",
        shadowSize: [0, 0],
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
      layer.on("click", () => setCurrentLocation(feature.properties.id))
      layer.on("mouseover", () => layer.openPopup())
      layer.on("mouseout", () => layer.closePopup())
    }
  },
})
