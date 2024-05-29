<script lang="ts">
  import type { components } from "$lib/openAPI.js"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let countries: components["schemas"]["Country"][] = []
  export let value: components["schemas"]["Country"] | null = null
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
  placeholder="Select a country"
/>
