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
    oninput?: (e: CustomEvent) => void
    onclear?: (e: CustomEvent) => void
  }

  let {
    countries = [],
    value = $bindable(),
    name = undefined,
    disabled = false,
    required = false,
    oninput,
    onclear,
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
  {oninput}
  {onclear}
  placeholder={$_("Select a country")}
/>
