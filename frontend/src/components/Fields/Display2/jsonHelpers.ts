import { _ } from "svelte-i18n"
import { get } from "svelte/store"

export function dateCurrentFormat(value: { date?: string; current?: boolean }): string {
  const $_ = get(_)

  if (!value.date && !value.current) return ""
  let ret = "["
  if (value.date) ret += value.date
  if (value.date && value.current) ret += ", "
  if (value.current) ret += $_("current")
  ret += "]"
  return ret
}

export const formatArea = (area: number): string =>
  (area / 10000)
    .toFixed(2)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, " ")
