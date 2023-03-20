import type { Feature, Point, Polygon } from "geojson"

export const isPoint = (feature: Feature): feature is Feature<Point> =>
  feature.geometry.type === "Point"
export const isPolygon = (feature: Feature): feature is Feature<Polygon> =>
  feature.geometry.type === "Polygon"
