<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Country } from "$lib/types/data"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let countries: Country[] = []
  export let value: Country | null = null
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
  placeholder={$_("Select a country")}
/>
