<script lang="ts">
  import Select from "svelte-select"
  import { _ } from "svelte-i18n"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string
  export let required = false
  export let disabled = false

  interface Item {
    value: string
    label: string
    group?: string
  }

  let items: Item[]
  $: items = (formfield.choices ?? [])
    // The literal translation strings are defined in apps/landmatrix/models/choices.py
    .map(i => ({ ...i, label: $_(i.label), group: i.group ? $_(i.group) : undefined }))
    .sort((a, b) => a.label.toLowerCase().localeCompare(b.label.toLowerCase()))

  let focused: boolean
</script>

<Select
  value={items.find(i => i.value === value)}
  bind:justValue={value}
  bind:focused
  {items}
  {required}
  {disabled}
  name={formfield.name}
  hasError={required && !value && !focused}
  showChevron
  groupBy={item => item.group}
/>
