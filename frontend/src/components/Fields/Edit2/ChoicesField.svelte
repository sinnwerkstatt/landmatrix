<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import type { ValueLabelEntry } from "$lib/stores"

  export let value: string | string[] | null

  interface Extras {
    multipleChoices?: boolean
    choices: ValueLabelEntry[]
    required?: boolean
    clearable?: boolean
  }

  export let extras: Extras = { choices: [] }

  $: multiple = !!extras.multipleChoices
  $: required = !!extras.required
  $: clearable = !!extras.clearable

  let focused: boolean

  const setMultiValue = (items: ValueLabelEntry[]) => {
    value = !items || items.length === 0 ? [] : items.map(i => i.value)
  }
  const setValue = (item: ValueLabelEntry) => {
    value = !item ? null : item.value
  }
</script>

<Select
  bind:focused
  {clearable}
  hasError={required && !value && !focused}
  items={extras.choices}
  groupBy={item => item.group}
  {multiple}
  on:input={e => (multiple ? setMultiValue : setValue)(e.detail)}
  placeholder={$_("Please select")}
  {required}
  showChevron
  value={multiple
    ? extras.choices.filter(c => (value || []).includes(c.value))
    : extras.choices.find(c => c.value === value)}
/>
