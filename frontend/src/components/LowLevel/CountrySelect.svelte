<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Country } from "$lib/types/data"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  interface Props {
    countries?: Country[]
    value?: Country | null
    name?: string | undefined
    disabled?: boolean
    required?: boolean
  }

  let {
    countries = [],
    value = $bindable(),
    name = undefined,
    disabled = false,
    required = false,
  }: Props = $props()
</script>

<VirtualListSelect
  bind:value
  items={countries}
  label="name"
  heightInPx={152}
  {name}
  {disabled}
  {required}
  on:input
  on:clear
  placeholder={$_("Select a country")}
/>
