import { _ } from "svelte-i18n"
import { get } from "svelte/store"

export function dateCurrentFormat(value: {
  date: string | null
  current: boolean
}): string {
  const $_ = get(_)

  if (!value.date && !value.current) return ""
  let ret = "["
  if (value.date) ret += value.date
  if (value.date && value.current) ret += ", "
  if (value.current) ret += $_("current")
  ret += "]"
  return ret
}

export function dateCurrentFormatStartEnd(value: {
  start_date: string | null
  end_date: string | null
  current: boolean
}): string {
  const $_ = get(_)

  if (!value.start_date && !value.end_date && !value.current) return ""
  let ret = "["
  if (value.start_date) ret += value.start_date
  if (value.start_date && value.end_date) ret += "–"
  if (value.end_date) ret += value.end_date
  if ((value.start_date || value.end_date) && value.current) ret += ", "
  if (value.current) ret += $_("current")
  ret += "]"
  return ret
}

export const formatArea = (area: number): string =>
  (area / 10000)
    .toFixed(2)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, " ")
