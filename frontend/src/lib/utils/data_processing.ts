import type { Contract, DataSource, Deal } from "$lib/types/deal"
import type { Involvement } from "$lib/types/investor"

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
    (Array.isArray(field) && field.length === 0)
  )
}

function sieveSubmodel(
  entry: Contract | DataSource | Location | Involvement,
  ignoreKeys = ["id", "role"],
) {
  return Object.entries(entry).filter(([k, v]) =>
    ignoreKeys.includes(k) ? false : !custom_is_null(v),
  )
}

export function isEmptySubmodel(entry: Contract | DataSource | Location): boolean {
  const fieldsWithValues = sieveSubmodel(entry)
  return fieldsWithValues.length === 0
}
export function removeEmptyEntries<
  T extends Contract | DataSource | Location | Involvement,
>(objectlist: T[]): T[] {
  // this function throws out any entries that have only an ID field and otherwise empty values.
  return objectlist.filter(con => sieveSubmodel(con).some(x => !!x))
}
