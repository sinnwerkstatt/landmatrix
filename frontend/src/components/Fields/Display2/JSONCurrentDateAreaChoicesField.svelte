<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateAreaChoicesFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"

  export let value: JSONCurrentDateAreaChoicesFieldType[] = []

  interface Extras {
    choices: ValueLabelEntry[]
  }

  export let extras: Extras = { choices: [] }
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>

      {#each val.choices ?? [] as v}
        {extras.choices.find(c => c.value === v)?.label ?? ""}
      {/each}
      <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
      <!--{val.choices.map(v => $_(flat_choices[v])).join(", ")}-->
      {#if val.area}
        ({val.area.toLocaleString("fr")}
        {$_("ha")})
      {/if}
    </li>
  {/each}
</ul>
