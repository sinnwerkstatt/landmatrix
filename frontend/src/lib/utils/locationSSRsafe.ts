import type { LatLngLiteral } from "leaflet"
import { LatLngBounds } from "leaflet?client"

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
