<script lang="ts">
  import Select from "svelte-select"
  import { _ } from "svelte-i18n"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string[] | undefined = undefined
  export let required = false

  interface Item {
    value: string
    label: string
    group?: string
  }
  let items: Item[]
  $: items = (formfield.choices ?? [])
    .map(i => ({ ...i, label: $_(i.label), group: i.group ? $_(i.group) : undefined }))
    .sort((a, b) => a.label.toLowerCase().localeCompare(b.label.toLowerCase()))

  const setValue = (items: Item[]) => {
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
  groupBy={item => item.group}
  name={formfield.name}
  hasError={required && !value && !focused}
  on:input={e => setValue(e.detail)}
  placeholder={$_("Please select")}
/>
