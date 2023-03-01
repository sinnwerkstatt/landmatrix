<script lang="ts">
  import Select from "svelte-select"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string
  export let required = false
  export let disabled = false

  let items
  $: items = Object.entries(formfield.choices).map(entry => ({
    value: entry[0],
    label: entry[1],
  }))
</script>

<div class="typed_choice_field">
  <Select
    value={items.find(i => i.value === value)}
    bind:justValue={value}
    {items}
    {required}
    {disabled}
    name={formfield.name}
    showChevron
  />
</div>
