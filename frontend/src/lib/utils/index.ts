import type { Deal } from "$lib/types/deal"
import type { Investor } from "$lib/types/investor"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type TableObj = Deal | Investor | { [key: string]: any }

function dotResolve(path: string, obj: TableObj) {
  if (!path.includes(".")) return obj[path]
  return path.split(".").reduce((prev, curr) => {
    return prev ? prev[curr] : null
  }, obj)
}

function _strCmp(a: string, b: string) {
  return a.toLocaleLowerCase().trim().localeCompare(b.toLocaleLowerCase().trim())
}

export const sortFn =
  (sortKey: string) =>
  (a: TableObj, b: TableObj): number => {
    const descending = sortKey.startsWith("-")
    let x, y
    // debugger;

    if (descending) {
      y = dotResolve(sortKey.substring(1), a)
      x = dotResolve(sortKey.substring(1), b)
    } else {
      x = dotResolve(sortKey, a)
      y = dotResolve(sortKey, b)
    }

    if (sortKey.includes("workflowinfos")) {
      if (x.length === 0) return -1
      if (y.length === 0) return 1
      return new Date(x[0].timestamp) - new Date(y[0].timestamp)
    }

    if (x === null || x === undefined) return -1
    if (y === null || y === undefined) return 1

    switch (typeof x) {
      case "number":
        return x - y
      case "string":
        return _strCmp(x, y)
      case "object":
        if (x.name) return _strCmp(x.name, y.name)
        if (x.username) return _strCmp(x.username, y.username)

        return x.length - y.length
    }

    return 0
  }

export function slugify(str: string) {
  return str
    .replace("ä", "ae")
    .replace("ö", "oe")
    .replace("ü", "ue")
    .replace("ß", "ss")
    .normalize("NFD") // split an accented letter in the base letter and the acent
    .replace(/[\u0300-\u036f]/g, "") // remove all previously split accents
    .replace(/\s+/g, "_") // separator
    .replace(/[^@_+.a-zA-Z0-9 -]/g, "") // remove all chars not letters, numbers and spaces (to be replaced)
    .trim()
}

export async function getCsrfToken() {
  return (await (await fetch(`/api/csrf_token/`)).json()).token
}
