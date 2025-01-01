import type { Country } from "$lib/types/data"

import { createCoordinatesMapLeaflet } from "$components/Map/utils"

describe("createCoordinatesMap", () => {
  test("Create empty map for empty country array", () => {
    expect(createCoordinatesMapLeaflet([])).toEqual({})
  })
  test("Create map of latitude longitude tuples", () => {
    expect(
      createCoordinatesMapLeaflet([
        { id: 1, point_lat: 0, point_lon: 34.99 } as Country,
        { id: 2, point_lat: -20.55, point_lon: 0.4 } as Country,
      ]),
    ).toEqual({
      1: [0, 34.99],
      2: [-20.55, 0.4],
    })
  })
})
