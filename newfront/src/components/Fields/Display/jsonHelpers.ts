// const myMixin = {
//   data() {
//     return {
//       current: -1,
//       vals:
//         this.value && this.value.length > 0
//           ? JSON.parse(JSON.stringify(this.value))
//           : [{}],
//     };
//   },
//   created() {
//     if (this.value) {
//       this.current = this.value.map((e) => e.current).indexOf(true);
//     }
//   },
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

export function mapChoices(choices, formfieldChoices) {
  let ret = ""
  if (choices instanceof Array) {
    ret += choices.map(v => formfieldChoices[v]).join(", ")
  } else {
    ret += formfieldChoices[choices]
  }
  return ret
}
