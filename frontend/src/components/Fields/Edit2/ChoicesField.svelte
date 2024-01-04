<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import type { ValueLabelEntry } from "$lib/stores"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: string | string[]
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let multiple = false
  export let choices: ValueLabelEntry[]

  let focused: boolean
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <Select
      value={choices.find(c => c.value === value)}
      bind:justValue={value}
      bind:focused
      items={choices}
      {multiple}
      showChevron
      placeholder={$_("Please select")}
    />
  </div>
</div>
