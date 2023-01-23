import { _ } from "svelte-i18n"
import { get } from "svelte/store"

export function dateCurrentFormat(value: { date: string; current?: boolean }): string {
  if (!value.date && !value.current) return ""
  let ret = "["
  if (value.date) ret += value.date
  if (value.date && value.current) ret += ", "
  if (value.current) ret += get(_)("current")
  ret += "]"
  return ret
}
