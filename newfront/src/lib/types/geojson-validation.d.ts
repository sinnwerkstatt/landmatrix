declare module "geojson-validation" {
  import type { FeatureCollection, Polygon, MultiPolygon } from "geojson";
  const isFeatureCollection: (object: any) => object is FeatureCollection;
  const isPolygon: (object: any) => object is Polygon;
  const isMultiPolygon: (object: any) => object is MultiPolygon;
}
