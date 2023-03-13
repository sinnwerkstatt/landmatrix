<script lang="ts">
  import Select from "svelte-select"
  import { _ } from "svelte-i18n"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string
  export let required = false
  export let disabled = false

  interface Item<T> {
    value: T
    label: string
  }

  let items: Item<string>[]
  $: items = Object.entries(formfield.choices).map(entry => ({
    value: entry[0],
    // The literal translation strings are defined in apps/landmatrix/models/choices.py
    label: $_(entry[1]),
  }))

  let focused
</script>

<div class="typed_choice_field">
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
  />
</div>
