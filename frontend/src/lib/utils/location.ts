import type { Point } from "geojson"
import type { GeoJSON, LatLngLiteral, Map } from "leaflet"
import { LatLngBounds } from "leaflet?client"

import type { AreaType, Location2, PointFeature } from "$lib/types/newtypes"

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
