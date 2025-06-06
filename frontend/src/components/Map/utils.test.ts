import type { Country } from "$lib/types/data"

import { createCoordinatesMap } from "$components/Map/utils"

describe("createCoordinatesMap", () => {
  test("Create empty map for empty country array", () => {
    expect(createCoordinatesMap([])).toEqual({})
  })
  test("Create map of latitude longitude tuples", () => {
    expect(
      createCoordinatesMap([
        { id: 1, point_lon: 0, point_lat: 34.99 } as Country,
        { id: 2, point_lon: -20.55, point_lat: 0.4 } as Country,
      ]),
    ).toEqual({
      1: [0, 34.99],
      2: [-20.55, 0.4],
    })
  })
})
