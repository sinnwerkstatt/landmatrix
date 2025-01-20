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
    oninput?: (e: CustomEvent) => void
    onclear?: (e: CustomEvent) => void
  }

  let {
    regions = [],
    value = $bindable(null),
    name = undefined,
    disabled = false,
    required = false,
    oninput,
    onclear,
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
  {oninput}
  {onclear}
  placeholder={$_("Select a region")}
/>
