<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import type { FormField } from "$components/Fields/fields"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"
  import PlaneIcon from "$components/icons/PlaneIcon.svelte"
  import WeightIcon from "$components/icons/WeightIcon.svelte"

  type JSONExportsFieldType = {
    current?: boolean
    area: number | null
    yield: number | null
    export: number | null
    choices: string[]
  }

  export let value: JSONExportsFieldType[] = []
  export let formfield: FormField

  $: flat_choices = formfield.choices
    ? Object.fromEntries(formfield.choices.map(c => [c.value, c.label]))
    : {}
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.choices}
        <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
        {val.choices.map(v => $_(flat_choices[v])).join(", ")}
      {/if}
        {#if val.area}
        <span>
          <CircleNotchIcon />
          {val.area.toLocaleString("fr")}
          {$_("ha")}
        </span>
      {/if}
      {#if val.yield}
        <span class="mx-2">
          <WeightIcon />
          {val.yield.toLocaleString("fr")}
          {$_("tons")}
        </span>
      {/if}
      {#if val.export}
        <span class="mx-2">
          <PlaneIcon />
          {val.export.toLocaleString("fr")} %
        </span>
      {/if}
    </li>
  {/each}
</ul>
