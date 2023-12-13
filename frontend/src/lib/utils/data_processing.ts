import type { Contract, DataSource, Deal } from "$lib/types/deal"
import type { Involvement } from "$lib/types/investor"

export type SubmodelEntry = Contract | DataSource | Location | Involvement

export function sum(items: Deal[], prop: keyof Deal): number {
  return items.reduce(function (a, b) {
    return a + (b[prop] as number)
  }, 0)
}

export function custom_is_null(field: unknown): boolean {
  return (
    field === undefined ||
    field === null ||
    field === "" ||
    (Array.isArray(field) && field.length === 0) ||
    // https://stackoverflow.com/questions/679915
    (typeof field === "object" &&
      Object.keys(field).length === 0 &&
      Object.getPrototypeOf(field) === Object.prototype)
  )
}
export const discardEmptyFields = (deal: Deal) =>
  Object.fromEntries(Object.entries(deal).filter(([, value]) => !custom_is_null(value)))

function sieveSubmodel(entry: SubmodelEntry, ignoreKeys = ["id", "nid", "role"]) {
  return Object.entries(entry).filter(([k, v]) =>
    ignoreKeys.includes(k) ? false : !custom_is_null(v),
  )
}

export function isEmptySubmodel(entry: SubmodelEntry): boolean {
  const fieldsWithValues = sieveSubmodel(entry)
  return fieldsWithValues.length === 0
}
export function removeEmptyEntries<T extends SubmodelEntry>(objectlist: T[]): T[] {
  // this function throws out any entries that have only an ID field and otherwise empty values.
  return objectlist.filter(con => sieveSubmodel(con).some(x => !!x))
}
