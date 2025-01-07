<script lang="ts">
  import type { Snippet } from "svelte"

  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  interface Extras {
    unit?: string
    placeholder?: string
    range?: [number, number]
  }

  interface Props {
    value: number | null
    fieldname: string
    extras?: Extras
    children?: Snippet
    onchange?: () => void
  }

  let {
    value = $bindable(),
    fieldname,
    extras = {},
    children,
    onchange,
  }: Props = $props()
  let min = $derived(extras?.range?.[0])
  let max = $derived(extras?.range?.[1])
</script>

<div class="flex items-center gap-4">
  <LowLevelDecimalField
    bind:value
    name={fieldname}
    unit={extras.unit}
    placeholder={extras.placeholder}
    {min}
    {max}
    {onchange}
  />
  {@render children?.()}
</div>
