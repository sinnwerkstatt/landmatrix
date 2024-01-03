export const createValueCopyNoNull = <T>(value: T[]): T[] => {
  return JSON.parse(JSON.stringify(value.length > 0 ? value : [{}]))
}
