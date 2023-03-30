<script lang="ts">
  import type { Country } from "$lib/types/wagtail"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let countries: Country[] = []
  export let value: Country | undefined = undefined
  export let name: string | undefined = undefined
  export let disabled = false
  export let required = false
</script>

<VirtualListSelect
  bind:value
  items={countries}
  label="name"
  {name}
  {disabled}
  {required}
  on:input
/>
