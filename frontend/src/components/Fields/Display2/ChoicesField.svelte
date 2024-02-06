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

  $: isMulti = (value: string | string[]): value is string[] => multipleChoices
</script>

{#if !value}
  -
{:else if isMulti(value)}
  {value.map(x => choices.find(c => c.value === x)?.label ?? "-").join(", ")}
{:else}
  {choices.find(c => c.value === value)?.label ?? ""}
{/if}
