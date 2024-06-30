import type { MultiPolygon, Point } from "geojson"
import {
  GeoJSON,
  geoJson,
  latLngBounds,
  LatLngBounds,
  type LatLngLiteral,
  type Layer,
  type Map,
} from "leaflet?client"

import type {
  Area,
  AreaFeature,
  AreaFeatureLayer,
  AreaType,
  Location2,
  PointFeature,
} from "$lib/types/data"
import { isEmptySubmodel } from "$lib/utils/dataProcessing"
import { createComponentAsDiv } from "$lib/utils/domHelpers"

import LocationAreaTooltip from "./LocationAreaTooltip.svelte"

const LOCATION_IGNORE_KEYS = ["dealversion"] satisfies (keyof Location2)[]

// explicitly set fields to null!
export const createLocation = (nid: string): Location2 => ({
  nid,
  id: null!,
  name: "",
  description: "",
  point: null,
  facility_name: "",
  level_of_accuracy: undefined,
  comment: "",
  areas: [],
  dealversion: null!,
})

export const isEmptyLocation = (location: Location2) =>
  isEmptySubmodel(location, LOCATION_IGNORE_KEYS)

// TODO: use $fieldChoices.area.type
export const AREA_TYPES = [
  "production_area",
  "contract_area",
  "intended_area",
] as const satisfies AreaType[]

export const AREA_TYPE_COLOR_MAP: { [key in AreaType]: string } = {
  contract_area: "#ff00ff",
  intended_area: "#66ff33",
  production_area: "#ff0000",
}

export const createPointFeature = (location: Location2): PointFeature => ({
  type: "Feature",
  geometry: location.point as Point,
  properties: {
    id: location.nid,
    level_of_accuracy: location.level_of_accuracy,
    name: location.name,
  },
})

export const createPointFeatures = (locations: readonly Location2[]): PointFeature[] =>
  locations.filter(l => l.point !== null).map(l => createPointFeature(l))

export const padBounds = (bounds: LatLngBounds): LatLngBounds => {
  const ne = bounds.getNorthEast()
  const sw = bounds.getSouthWest()

  if (ne.equals(sw)) {
    const margin = 0.2

    return new LatLngBounds(
      { lat: ne.lat + margin, lng: ne.lng + margin } as LatLngLiteral,
      { lat: sw.lat - margin, lng: sw.lng - margin } as LatLngLiteral,
    )
  }

  return bounds.pad(0.2)
}

export const fitBounds = (map: Map) => {
  let bounds = latLngBounds([])
  map.eachLayer(
    l => (bounds = l instanceof GeoJSON ? l.getBounds().extend(bounds) : bounds),
  )
  if (bounds.isValid()) {
    map.fitBounds(padBounds(bounds))
  }
}

export const createAreaFeaturesLayer = (features: AreaFeature[]): AreaFeatureLayer =>
  geoJson(features, {
    style: feature => ({
      weight: 1.5,
      color: "black",
      dashArray: "5, 5",
      dashOffset: "0",
      fillColor: AREA_TYPE_COLOR_MAP[feature!.properties.type],
      fillOpacity: 0.4,
    }),
    onEachFeature: (feature, layer: Layer) => {
      const tooltipElement = createComponentAsDiv(LocationAreaTooltip, { feature })
      layer.bindPopup(tooltipElement, {
        keepInView: true,
        autoPanPaddingTopLeft: [20, 20],
        autoPanPaddingBottomRight: [20, 100],
      })
    },
  })

export const areaToFeature = (area: Area): AreaFeature => ({
  type: "Feature",
  geometry: area.area as MultiPolygon,
  id: area.nid,
  properties: {
    id: area.nid,
    type: area.type,
    date: area.date ?? "",
    current: !!area.current,
    visible: true,
  },
})

// export const featureToArea = (feature: AreaFeature): Area => ({
//   id: feature.properties.id,
//   type: feature.properties.type,
//   date: feature.properties.date,
//   current: feature.properties.current,
//   area: feature.geometry,
// })
