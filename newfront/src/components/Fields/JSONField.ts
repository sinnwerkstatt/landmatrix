export const createValueCopy = <T>(value: T[] | null): T[] => {
  return JSON.parse(JSON.stringify(value ?? [{}]))
}

export const syncValue = <T>(filter_fn: (val: T) => boolean, copy: T[]): T[] | null => {
  const filtered = copy.filter(filter_fn)
  return filtered.length > 0 ? filtered : null
}
