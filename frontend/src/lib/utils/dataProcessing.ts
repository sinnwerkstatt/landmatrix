const SUBMODEL_ID_KEYS = ["id", "nid"] as const

export type SubmodelIdKeys = (typeof SUBMODEL_ID_KEYS)[number]
export type Submodel = object & { [key in SubmodelIdKeys]?: number | string | null }

export const sum = <T extends Submodel>(items: T[], prop: keyof T): number =>
  items.reduce(function (a, b) {
    return a + (b[prop] as number)
  }, 0)

export const customIsNull = (field: unknown): boolean =>
  field === undefined ||
  field === null ||
  field === "" ||
  (Array.isArray(field) && field.length === 0) ||
  // https://stackoverflow.com/questions/679915
  (typeof field === "object" &&
    Object.keys(field).length === 0 &&
    Object.getPrototypeOf(field) === Object.prototype)

export const sieveSubmodel = <T extends Submodel>(
  entry: T,
  ignoreKeys: string[] = [],
) =>
  Object.entries(entry).filter(([k, v]) => !ignoreKeys.includes(k) && !customIsNull(v))

export const isEmptySubmodel = <T extends Submodel>(
  entry: T,
  ignoreKeys: string[] = [],
): boolean => sieveSubmodel(entry, [...SUBMODEL_ID_KEYS, ...ignoreKeys]).length === 0

export const discardEmptySubmodels = <T extends Submodel>(
  entries: T[],
  ignoreKeys: string[] = [],
): T[] => entries.filter(entry => !isEmptySubmodel(entry, ignoreKeys))
