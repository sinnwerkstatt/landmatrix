export function thousandsep(value: number): string {
  if (value === undefined) return "";
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}
