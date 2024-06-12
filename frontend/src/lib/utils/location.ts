import type { Point } from "geojson"
import type { GeoJSON, LatLngLiteral, Map } from "leaflet?client"
import { geoJson, LatLngBounds } from "leaflet?client"

import type {
  Area,
  AreaFeature,
  AreaFeatureLayer,
  AreaType,
  Location2,
  PointFeature,
} from "$lib/types/newtypes"

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

export const createPointFeatures = (locations: Location2[]): PointFeature[] =>
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

  return bounds.pad(0.8)
}

export const fitBounds = (geoJson: GeoJSON, map: Map): void => {
  const bounds = geoJson.getBounds()
  bounds.isValid() && map.fitBounds(padBounds(bounds), { duration: 1 })
}

export const createAreaFeaturesLayer = (
  features: AreaFeature[],
  isSelectedEntry: boolean,
): AreaFeatureLayer =>
  geoJson(features, {
    filter: feature => feature.properties.visible,
    style: feature => ({
      weight: 1.5,
      color: "black",
      dashArray: "5, 5",
      dashOffset: "0",
      fillColor: isSelectedEntry
        ? feature
          ? AREA_TYPE_COLOR_MAP[feature.properties.type]
          : ""
        : "grey",
      fillOpacity: 0.4,
    }),
  })

export const areaToFeature = (area: Area): AreaFeature => ({
  type: "Feature",
  geometry: area.area,
  properties: {
    id: area.id as number,
    type: area.type,
    date: area.date,
    current: area.current,
    visible: area.current,
  },
})

export const featureToArea = (feature: AreaFeature): Area => ({
  id: feature.properties.id,
  type: feature.properties.type,
  date: feature.properties.date,
  current: feature.properties.current,
  area: feature.geometry,
})

export const isVisible = (feature: AreaFeature): boolean => feature.properties.visible
export const isCurrent = (feature: AreaFeature): boolean => !!feature.properties.current
