<script lang="ts">
  import type { ValueLabelEntry } from "$lib/stores"

  interface Extras {
    multipleChoices?: boolean
    choices: ValueLabelEntry[]
  }

  interface Props {
    value: string | string[]
    extras?: Extras
  }

  let { value, extras = { choices: [] } }: Props = $props()

  let multipleChoices = $derived(extras.multipleChoices ?? false)
  let choices = $derived(extras.choices ?? [])

  let isMulti = (_v: string | string[]): _v is string[] => multipleChoices
</script>

{#if !value}
  -
{:else if isMulti(value)}
  {value.map(x => choices.find(c => c.value === x)?.label ?? "-").join(", ")}
{:else}
  {choices.find(c => c.value === value)?.label ?? ""}
{/if}
