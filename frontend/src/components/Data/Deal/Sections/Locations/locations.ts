import { Overlay, type Feature } from "ol"
import type { MultiPolygon, Point } from "ol/geom"
import { mount } from "svelte"

import type { components } from "$lib/openAPI"
import type { Location } from "$lib/types/data"
import { isEmptySubmodel } from "$lib/utils/dataProcessing"

import LocationAreaTooltip from "$components/Data/Deal/Sections/Locations/LocationAreaTooltip.svelte"
import LocationTooltip from "$components/Data/Deal/Sections/Locations/LocationTooltip.svelte"

const LOCATION_IGNORE_KEYS = ["dealversion"] satisfies (keyof Location)[]

// explicitly set fields to null!
export const createLocation = (nid: string): Location => ({
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

export const isEmptyLocation = (location: Location) =>
  isEmptySubmodel(location, LOCATION_IGNORE_KEYS)

export const AREA_TYPES = [
  "production_area",
  "contract_area",
  "intended_area",
] as const satisfies components["schemas"]["LocationAreaTypeEnum"][]

export const AREA_TYPE_COLOR_MAP: {
  [key in components["schemas"]["LocationAreaTypeEnum"]]: string
} = {
  contract_area: "#aa70dd",
  intended_area: "#a0d875",
  production_area: "#e86a6a",
}

export async function createLocationTooltipOverlay(feature: Feature<Point>) {
  const containerDiv = document.createElement("div")
  mount(LocationTooltip, { target: containerDiv, props: { feature } })
  return new Overlay({
    element: containerDiv,
    position: feature.getGeometry()!.getCoordinates(),
    positioning: "bottom-center",
    offset: [-30, -30, -30, -30],
    autoPan: { animation: { duration: 300 } },
  })
}
export async function createPolygonTooltipOverlay(feature: Feature<MultiPolygon>) {
  const containerDiv = document.createElement("div")
  mount(LocationAreaTooltip, { target: containerDiv, props: { feature } })
  return new Overlay({
    element: containerDiv,
    position: feature.getGeometry()!.getFirstCoordinate(),
    positioning: "bottom-center",
    offset: [-30, -30, -30, -30],
    autoPan: { animation: { duration: 300 } },
  })
}
