import type { Location2 } from "$lib/types/data"
import { isEmptySubmodel } from "$lib/utils/dataProcessing"

const LOCATION_IGNORE_KEYS = ["dealversion"] satisfies (keyof Location2)[]

// explicitly set fields to null!
export const createLocation = (nid: string): Location2 => ({
  nid,
  id: null!,
  name: "",
  description: "",
  point: null,
  facility_name: "",
  level_of_accuracy: undefined,
  comment: "",
  areas: [],
  dealversion: null!,
})

export const isEmptyLocation = (location: Location2) =>
  isEmptySubmodel(location, LOCATION_IGNORE_KEYS)
