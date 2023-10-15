<script lang="ts">
  import Select from "svelte-select"
  import { _ } from "svelte-i18n"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string[] | undefined = undefined
  export let required = false

  interface Item<T> {
    value: T
    label: string
  }
  let items: Item<string>[]
  $: items = Object.entries(formfield.choices).map((entry: [string, string]) => ({
    value: entry[0],
    // The literal translation strings are defined in apps/landmatrix/models/choices.py
    label: $_(entry[1]),
  }))

  const setValue = (items: Item<string>[]) => {
    // set undefined on empty value array
    value = !items || items.length === 0 ? undefined : items.map(i => i.value)
  }

  let focused: boolean
</script>

<Select
  value={items.filter(i => (value || []).includes(i.value))}
  bind:focused
  {items}
  {required}
  multiple
  showChevron
  placeholder={$_("Please select")}
  name={formfield.name}
  hasError={required && !value && !focused}
  on:input={e => setValue(e.detail)}
/>
