import type { Country } from "$lib/types/data"

export const createCoordinatesMap = (
  countries: Country[],
): {
  [key: number]: [lat: number, long: number]
} =>
  countries.reduce(
    (acc, { id, point_lon, point_lat }) => ({
      ...acc,
      [id]: [point_lon, point_lat],
    }),
    {},
  )
