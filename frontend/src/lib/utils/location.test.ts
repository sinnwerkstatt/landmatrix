import { latLng, latLngBounds } from "leaflet?client"

import { ACCURACY_LEVEL, type Location2 } from "$lib/types/newtypes"

import { createPointFeature, createPointFeatures, padBounds } from "./location"

const LAGOS_NIGERIA = latLng(6.455027, 3.384082)
const ABUJA_NIGERIA = latLng(9.4, 7.29)

describe("padBounds", () => {
  test("adds padding around a point - 0d bound (SW equals NE)", () => {
    const bounds = latLngBounds(LAGOS_NIGERIA, LAGOS_NIGERIA)

    expect(padBounds(bounds).contains(bounds)).toBeTruthy()
    expect(padBounds(bounds).equals(bounds)).toBeFalsy()
  })
  test("adds padding around a square - 2d bound", () => {
    const bounds = latLngBounds(LAGOS_NIGERIA, ABUJA_NIGERIA)

    expect(padBounds(bounds).contains(bounds)).toBeTruthy()
    expect(padBounds(bounds).equals(bounds)).toBeFalsy()
  })
})

describe("createPointFeature", () => {
  test("Map location to geojson point feature with properties", () => {
    const location: Location2 = {
      nid: "nanoID",
      name: "I have a name?",
      description: "A vast location.",
      point: {
        type: "Point",
        coordinates: [6.455027, 3.384082],
      },
      facility_name: "Invisible Inc.",
      level_of_accuracy: ACCURACY_LEVEL.APPROXIMATE_LOCATION,
      comment: "BLA",
      areas: [],
    }

    const feature = createPointFeature(location)

    expect(feature.geometry).toBe(location.point)

    expect(feature.properties.id).toBe(location.nid)
    expect(feature.properties.name).toBe(location.name)
    expect(feature.properties.level_of_accuracy).toBe(location.level_of_accuracy)
  })
})

describe("createPointFeatures", () => {
  test("Skip locations with null points", () => {
    const locations = [
      { nid: "first", point: null },
      { nid: "second", point: { type: "Point", coordinates: [6.455027, 3.384082] } },
      { nid: "third", point: null },
    ] satisfies Partial<Location2>[] as Location2[]

    expect(createPointFeatures(locations)).toHaveLength(1)
    expect(createPointFeatures(locations)[0].properties.id).toBe("second")
  })
})
