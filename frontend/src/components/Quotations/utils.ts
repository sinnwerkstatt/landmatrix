export const mergeKeys = (obj1?: object, obj2?: object) => [
  ...new Set([...Object.keys(obj1 ?? {}), ...Object.keys(obj2 ?? {})]),
]
