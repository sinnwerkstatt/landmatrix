<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONCurrentDateAreaFieldType } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"

  export let value: JSONCurrentDateAreaFieldType = []

  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <ul>
        {#each value ?? [] as val}
          <li class:font-bold={val.current}>
            <span>{dateCurrentFormat(val)}</span>

            <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
            <!--{val.choices.map(v => $_(flat_choices[v])).join(", ")}-->
            {#if val.area}
              (
              <CircleNotchIcon />
              {val.area.toLocaleString("fr")}
              {$_("ha")})
            {/if}
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}
