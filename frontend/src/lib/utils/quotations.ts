type ObjWithNid = Record<"nid", string>

// TODO: Remove
export type Quotations<T extends ObjWithNid = ObjWithNid> = {
  [key: string]: T[] | Quotations<T>
}

export function getQuotations<T extends ObjWithNid>(
  input: Quotations<T>,
  path: (string | number)[],
): T[] | Quotations<T> {
  function recurse(
    current: Quotations<T> | T[] | undefined,
    depth: number,
  ): T[] | Quotations<T> {
    if (depth === path.length) {
      return current ?? []
    }

    const key = path[depth]

    if (typeof current !== "object" || current === null || !(key in current)) {
      return []
    }

    return recurse((current as Quotations<T>)[key], depth + 1)
  }

  return recurse(input, 0)
}

export function setQuotations<T extends ObjWithNid>(
  input: Quotations<T>,
  path: (string | number)[],
  value: T[] | Quotations<T>,
): Quotations<T> {
  function recurse(current: Quotations<T>, depth: number): Quotations<T> {
    const key = path[depth]

    if (depth === path.length - 1) {
      return { ...current, [key]: value }
    }

    const nextLevel =
      typeof current[key] === "object" && !Array.isArray(current[key])
        ? (current[key] as Quotations<T>)
        : {}

    return {
      ...current,
      [key]: recurse(nextLevel, depth + 1),
    }
  }

  return recurse(input, 0)
}

export function removeQuotations<T extends ObjWithNid>(
  input: Quotations<T>,
  targetNid: string,
): Quotations<T> {
  function recurse(current: Quotations<T>): Quotations<T> {
    const result: Quotations<T> = {}

    for (const [key, value] of Object.entries(current)) {
      if (Array.isArray(value)) {
        result[key] = value.filter(item => item.nid !== targetNid)
      } else {
        result[key] = recurse(value as Quotations<T>)
      }
    }

    return result
  }

  return recurse(input)
}

export function cleanEmptyBranches<T extends ObjWithNid>(
  input: Quotations<T>,
): Quotations<T> {
  function recurse(current: Quotations<T>): Quotations<T> | undefined {
    const result: Quotations<T> = {}

    for (const [key, value] of Object.entries(current)) {
      if (Array.isArray(value)) {
        if (value.length > 0) {
          result[key] = value
        }
      } else {
        const cleaned = recurse(value as Quotations<T>)
        if (cleaned !== undefined) {
          result[key] = cleaned
        }
      }
    }

    return Object.keys(result).length > 0 ? result : undefined
  }

  return recurse(input) ?? {}
}

export function setAndCleanQuotations<T extends ObjWithNid>(
  input: Quotations<T>,
  path: (string | number)[],
  value: T[] | Quotations<T>,
): Quotations<T> {
  if (path.length === 0) {
    return input
  }

  return cleanEmptyBranches(setQuotations(input, path, value))
}

export function removeAndCleanQuotations<T extends ObjWithNid>(
  input: Quotations<T>,
  targetNid: string,
): Quotations<T> {
  return cleanEmptyBranches(removeQuotations(input, targetNid))
}
