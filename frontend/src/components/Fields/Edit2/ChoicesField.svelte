<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import type { ValueLabelEntry } from "$lib/stores"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: string | string[] | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let multiple = false
  export let choices: ValueLabelEntry[]
  export let required = false
  export let clearable = false

  let focused: boolean

  const setMultiValue = (items: ValueLabelEntry[]) => {
    value = !items || items.length === 0 ? [] : items.map(i => i.value)
  }
  const setValue = (item: ValueLabelEntry) => {
    value = !item ? null : item.value
  }
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <Select
      value={multiple
        ? choices.filter(c => (value || []).includes(c.value))
        : choices.find(c => c.value === value)}
      bind:focused
      items={choices}
      {multiple}
      {required}
      {clearable}
      showChevron
      hasError={required && !value && !focused}
      on:input={e => (multiple ? setMultiValue : setValue)(e.detail)}
      placeholder={$_("Please select")}
    />
  </div>
</div>
