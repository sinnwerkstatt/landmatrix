import type { TableItem } from "$components/Table/Table.svelte"

export const sortFn =
  (sortKey: string) =>
  (a: TableItem, b: TableItem): number => {
    const descending = sortKey.startsWith("-")
    let x, y
    // debugger;

    if (descending) {
      y = _dotResolve(sortKey.substring(1), a)
      x = _dotResolve(sortKey.substring(1), b)
    } else {
      x = _dotResolve(sortKey, a)
      y = _dotResolve(sortKey, b)
    }

    if (sortKey.includes("workflowinfos")) {
      if (x.length === 0) return -1
      if (y.length === 0) return 1
      return (
        new Date(x[0].timestamp as string).getTime() -
        new Date(y[0].timestamp as string).getTime()
      )
    }

    if (x === null || x === undefined) return -1
    if (y === null || y === undefined) return 1

    switch (typeof x) {
      case "boolean":
        return x === y ? 0 : x ? -1 : 1
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

function _dotResolve(path: string, obj: TableItem) {
  if (!path.includes(".")) return obj[path]
  return path.split(".").reduce((prev, curr) => {
    return prev ? prev[curr] : null
  }, obj)
}

function _strCmp(a: string, b: string) {
  return a.toLocaleLowerCase().trim().localeCompare(b.toLocaleLowerCase().trim())
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

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number = 300,
): T {
  let timeout: NodeJS.Timeout

  console.log("running the bouncei")

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return function (this: any, ...args: Parameters<T>): ReturnType<T> {
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const context = this
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(context, args), wait)
    return undefined as unknown as ReturnType<T>
  } as T
}
