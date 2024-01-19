<script lang="ts">
  import type { ValueLabelEntry } from "$lib/stores"

  export let value: string | string[]

  interface Extras {
    multipleChoices?: boolean
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }

  $: multipleChoices = extras.multipleChoices ?? false
  $: choices = extras.choices ?? []

  const isMulti = (value: string | string[]): value is string[] => multipleChoices

  function enrichValue(value: string | string[]) {
    if (!value) return "—"
    if (isMulti(value)) {
      if (choices.length > 0) {
        console.log(choices)
        console.log(value)
        return value.map(x => choices.find(c => c.value === x)?.label ?? "-").join(", ")
      } else return value.join(", ")
    } else {
      if (choices.length > 0) return choices.find(c => c.value === value)?.label ?? ""
      else return value
    }
  }
</script>

{enrichValue(value)}
