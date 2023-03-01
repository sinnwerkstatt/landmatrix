<script lang="ts">
  import Select from "svelte-select"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string[] | undefined = undefined
  export let required = false

  interface Item<T> {
    value: T
    label: string
  }
  const items: Item<string>[] = Object.entries(formfield.choices).map(
    (entry: [string, string]) => ({
      value: entry[0],
      label: entry[1],
    }),
  )

  const setValue = (items: Item<string>[]) => {
    // set undefined on empty value array
    value = !items || items.length === 0 ? undefined : items.map(i => i.value)
  }

  let focused
</script>

<div class="typed_choices_field">
  <Select
    value={items.filter(i => (value || []).includes(i.value))}
    bind:focused
    {items}
    {required}
    multiple
    showChevron
    name={formfield.name}
    hasError={required && !value && !focused}
    on:input={e => setValue(e.detail)}
  />
</div>
