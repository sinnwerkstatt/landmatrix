import type { Point } from "geojson"
import * as L from "leaflet?client"

import type { AreaType } from "$lib/types/deal"
import type { AreaFeature, Location2, PointFeature } from "$lib/types/newtypes"

import LocationLegend from "$components/Deal/LocationLegend.svelte"
import LocationTooltip from "$components/Deal/LocationTooltip.svelte"

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

export const createTooltip = (feature: PointFeature | AreaFeature): HTMLElement => {
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
