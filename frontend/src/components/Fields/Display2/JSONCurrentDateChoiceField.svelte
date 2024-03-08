<script lang="ts">
  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"

  export let value: JSONCurrentDateChoiceFieldType[] = []

  interface Extras {
    choices?: ValueLabelEntry[]
  }

  export let extras: Extras = {}
  $: choices = extras.choices ?? []
</script>

<ul>
  {#each value as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {choices.find(c => c.value === val.choice)?.label ?? val.choice ?? ""}
    </li>
  {/each}
</ul>
