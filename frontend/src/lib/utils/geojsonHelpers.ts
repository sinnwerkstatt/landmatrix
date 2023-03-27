import type {
  Feature,
  FeatureCollection,
  GeoJsonProperties,
  Geometry,
  Point,
  Polygon,
  MultiPolygon,
  MultiPoint,
} from "geojson"
import * as R from "ramda"

import { newNanoid } from "$lib/helpers"

export const upsertProperties = R.curry(
  (props: object, feature: Feature): Feature => ({
    ...feature,
    properties: {
      ...feature.properties,
      ...props,
    },
  }),
)

export const setProperty = R.curry(
  /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
  (propName: string, propValue: any, feature: Feature): Feature => ({
    ...feature,
    properties: {
      ...feature.properties,
      [propName]: propValue,
    },
  }),
)

export const addTempIds = <T extends Feature>(features: T[]): (T & { id: string })[] =>
  features.reduce((acc: (T & { id: string })[], val: T) => {
    const existingIds: string[] = acc.map(feature => feature.id as string)
    return [...acc, { ...val, id: newNanoid(existingIds) }]
  }, [])

export const createFeatureCollection = <
  G extends Geometry | null = Geometry,
  P = GeoJsonProperties,
>(
  features: Feature<G, P>[],
): FeatureCollection<G, P> => ({
  type: "FeatureCollection",
  features,
})

export const isPoint = (feature: Feature): feature is Feature<Point | MultiPoint> =>
  feature.geometry.type === "Point"

export const isPolygon = (
  feature: Feature,
): feature is Feature<Polygon | MultiPolygon> =>
  feature.geometry.type === "Polygon" || feature.geometry.type === "MultiPolygon"
