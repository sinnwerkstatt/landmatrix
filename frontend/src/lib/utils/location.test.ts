import { latLng, latLngBounds } from "leaflet"

import type { LocationWithCoordinates } from "$lib/types/deal"
import { ACCURACY_LEVEL } from "$lib/types/deal"

import { createPointFeature, isLocationWithCoordinates, padBounds } from "./location"

const LAGOS_NIGERIA = latLng(6.455027, 3.384082)
const ABUJA_NIGERIA = latLng(9.4, 7.29)

describe("location utils", () => {
  describe("padBounds", () => {
    test("NE equal SW", () => {
      const bounds = latLngBounds(LAGOS_NIGERIA, LAGOS_NIGERIA)

      expect(padBounds(bounds).contains(bounds)).toBeTruthy()
      expect(padBounds(bounds).equals(bounds)).toBeFalsy()
    })
    test("NE not equal SW", () => {
      const bounds = latLngBounds(LAGOS_NIGERIA, ABUJA_NIGERIA)

      expect(padBounds(bounds).contains(bounds)).toBeTruthy()
      expect(padBounds(bounds).equals(bounds)).toBeFalsy()
    })
  })

  test("createPointFeature", () => {
    const location: LocationWithCoordinates = {
      id: "someUniqueId1234",
      point: {
        lat: 6.455027,
        lng: 3.384082,
      },
      level_of_accuracy: ACCURACY_LEVEL.COORDINATES,
    }
    const feature = createPointFeature(location)

    expect(feature.geometry.coordinates[0]).toBe(location.point.lng)
    expect(feature.geometry.coordinates[1]).toBe(location.point.lat)

    expect(feature.properties.id).toBe(location.id)
    expect(feature.properties.level_of_accuracy).toBe(location.level_of_accuracy)
  })

  test("isLocationWithCoordinates", () => {
    expect(
      isLocationWithCoordinates({
        id: "someUniqueId1234",
      }),
    ).toBeFalsy()

    expect(
      isLocationWithCoordinates({
        id: "someUniqueId1234",
        point: {} as LocationWithCoordinates["point"],
      }),
    ).toBeFalsy()

    expect(
      isLocationWithCoordinates({
        id: "someUniqueId1234",
        point: {
          lat: 6.455027,
          lng: 3.384082,
        },
      }),
    ).toBeFalsy()

    expect(
      isLocationWithCoordinates({
        id: "someUniqueId1234",
        point: {
          lat: 6.455027,
          lng: 3.384082,
        },
        level_of_accuracy: ACCURACY_LEVEL.COORDINATES,
      }),
    ).toBeTruthy()
  })
})
