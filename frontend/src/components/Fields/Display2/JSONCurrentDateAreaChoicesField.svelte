<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateAreaChoicesFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"

  export let value: JSONCurrentDateAreaChoicesFieldType[] = []

  interface Extras {
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }

  const getLabel = (value: string) =>
    extras.choices.find(c => value === c.value)?.label ?? value
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>

      {#if val.choices && extras.choices.length}
        <span>
          {val.choices.map(getLabel).join(", ")}
        </span>
      {/if}
      {#if val.area}
        ({val.area.toLocaleString("fr").replace(",", ".")}
        {$_("ha")})
      {/if}
    </li>
  {/each}
</ul>
