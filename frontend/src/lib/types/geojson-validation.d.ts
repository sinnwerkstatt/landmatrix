declare module "geojson-validation" {
  import type { FeatureCollection, Polygon, MultiPolygon } from "geojson"
  /* eslint-disable @typescript-eslint/no-explicit-any */
  const isFeatureCollection: (object: any) => object is FeatureCollection
  const isPolygon: (object: any) => object is Polygon
  const isMultiPolygon: (object: any) => object is MultiPolygon
  /* eslint-enable @typescript-eslint/no-explicit-any */
}
