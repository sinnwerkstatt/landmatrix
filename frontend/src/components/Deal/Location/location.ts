import * as L from "leaflet"
import type { Feature, Point } from "geojson"

import type { Location, LocationWithCoordinates, FeatureProps } from "$lib/types/deal"

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

export const isMarker = (layer: L.Layer): layer is L.Marker => layer instanceof L.Marker
