<script lang="ts">
  import type { ValueLabelEntry } from "$lib/stores"
  import type { JSONCurrentDateChoiceFieldType } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: JSONCurrentDateChoiceFieldType = []

  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let choices: ValueLabelEntry[]

  // $: flat_choices = formfield.choices
  //   ? Object.fromEntries(formfield.choices.map(c => [c.value, c.label]))
  //   : {}
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
            {choices.find(c => c.value === val.choice)?.label ?? ""}
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}
