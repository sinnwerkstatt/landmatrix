import type { FeatureCollection, GeoJsonObject, Geometry, Position } from "geojson"
import gjv from "geojson-validation"

const areAllFeaturesPolygons = (data: FeatureCollection) =>
  data.features.every(
    feature => gjv.isPolygon(feature.geometry) || gjv.isMultiPolygon(feature.geometry),
  )

const isSingleFeature = (data: FeatureCollection) => data.features.length === 1

// custom logic to validate long lat values
const isValidLongitude = (longitude: number) => -180 <= longitude && longitude <= 180
const isValidLatitude = (latitude: number) => -90 <= latitude && latitude <= 90
const isValidLongLatPostion = (position: Position) =>
  isValidLongitude(position[0]) && isValidLatitude(position[1])

type NestedCoordinates<T> = T | NestedCoordinates<T>[]
const areValidLongLatCoordinates = (
  coordinates: NestedCoordinates<Position>,
  level: number,
): boolean => {
  if (level > 0) {
    return (coordinates as Position[]).every(nested =>
      areValidLongLatCoordinates(nested, level - 1),
    )
  }
  return isValidLongLatPostion(coordinates as Position)
}

const isValidLongLatGeometry = (geometry: Geometry): boolean => {
  if (geometry.type === "GeometryCollection") {
    return geometry.geometries.every(isValidLongLatGeometry)
  }
  if (geometry.type === "Polygon") {
    return areValidLongLatCoordinates(geometry.coordinates, 2)
  }
  if (geometry.type === "MultiPolygon") {
    return areValidLongLatCoordinates(geometry.coordinates, 3)
  }
  if (geometry.type === "Point") {
    return areValidLongLatCoordinates(geometry.coordinates, 0)
  }
  if (geometry.type === "MultiPoint") {
    return areValidLongLatCoordinates(geometry.coordinates, 1)
  }
  if (geometry.type === "LineString") {
    return areValidLongLatCoordinates(geometry.coordinates, 1)
  }
  if (geometry.type === "MultiLineString") {
    return areValidLongLatCoordinates(geometry.coordinates, 2)
  }
  return false
}

const hasValidLongLatValues = (data: FeatureCollection): boolean => {
  return data.features.every(feature => isValidLongLatGeometry(feature.geometry))
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type ValidatorFn = (data: any) => boolean

const validators: [ValidatorFn, string][] = [
  [gjv.isFeatureCollection, "Data is not a valid FeatureCollection."],
  [areAllFeaturesPolygons, "Not all features are of type Polygons or MultiPolygon."],
  [isSingleFeature, "Please upload one feature at a time."],
  [
    hasValidLongLatValues,
    "Polygon coordinate are not given as Longitude (-180 to 180) " +
      "Latitude (-90 to 90) positions.",
  ],
]

export const validate = (data: GeoJsonObject): void => {
  for (const [validator, message] of validators) {
    if (!validator(data)) {
      throw new Error(message)
    }
  }
}
