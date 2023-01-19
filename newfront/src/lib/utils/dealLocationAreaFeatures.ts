import type { Feature } from "geojson"

import type {
  AreaFeature,
  AreaFeatureCollection,
  AreaType,
  Location,
} from "$lib/types/deal"

const createEmptyFeatureCollection = (): AreaFeatureCollection => ({
  type: "FeatureCollection",
  features: [],
})

// property setters
export const setAreaTypeProperty = (
  areaType: AreaType,
  feature: Feature,
): AreaFeature => ({
  ...feature,
  properties: { type: areaType },
})

export const setCurrentProperty =
  (current: number) =>
  (feature: Feature, index: number): AreaFeature => ({
    ...feature,
    properties: {
      ...feature.properties,
      current: index === current ? true : undefined,
    },
  })

// feature utils
export const getFeatures = (areaType: AreaType, location: Location): AreaFeature[] => {
  const activeAreas = location.areas ?? createEmptyFeatureCollection()

  return activeAreas.features.filter(feature => feature.properties.type === areaType)
}

export const setFeatures = (
  areaType: AreaType,
  location: Location,
  features: AreaFeature[],
): void => {
  const activeAreas = location.areas ?? createEmptyFeatureCollection()

  const otherFeatures = activeAreas.features.filter(
    feature => feature.properties.type !== areaType,
  )

  activeAreas.features = [...features, ...otherFeatures]
  location.areas = activeAreas.features.length > 0 ? activeAreas : undefined
}
