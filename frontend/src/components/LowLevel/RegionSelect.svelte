<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Region } from "$lib/types/data"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let regions: Region[] = []
  export let value: Region | null = null
  export let name: string | undefined = undefined
  export let disabled = false
  export let required = false
</script>

<VirtualListSelect
  bind:value
  id="region-select"
  items={regions}
  label="name"
  heightInPx={152}
  {name}
  {disabled}
  {required}
  on:input
  on:clear
  placeholder={$_("Select a region")}
/>
