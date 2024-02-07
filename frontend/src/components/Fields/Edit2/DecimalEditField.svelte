<script lang="ts">
  import LowLevelDecimalField from "$components/Fields/Edit2/LowLevelDecimalField.svelte"

  export let value: number | null
  export let fieldname: string

  interface Extras {
    unit?: string
    placeholder?: string
    range?: [number, number]
  }

  export let extras: Extras = {}
  $: min = extras?.range?.[0]
  $: max = extras?.range?.[1]
</script>

<div class="flex items-center gap-4">
  <LowLevelDecimalField
    bind:value
    name={fieldname}
    unit={extras.unit}
    placeholder={extras.placeholder}
    {min}
    {max}
  />
  <slot />
</div>
