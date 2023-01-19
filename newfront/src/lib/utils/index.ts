import type { Deal } from "$lib/types/deal"
import type { Investor } from "$lib/types/investor"

type TableObj = Deal | Investor | { [key: string]: any }

function dotResolve(path: string, obj: TableObj) {
  if (!path.includes(".")) return obj[path]
  return path.split(".").reduce(function (prev, curr) {
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
