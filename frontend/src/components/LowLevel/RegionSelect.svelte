<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Region } from "$lib/types/data"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  interface Props {
    regions?: Region[]
    value?: Region | null
    name?: string | undefined
    disabled?: boolean
    required?: boolean
  }

  let {
    regions = [],
    value = $bindable(null),
    name = undefined,
    disabled = false,
    required = false,
  }: Props = $props()
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
