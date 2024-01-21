<script lang="ts">
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"

  export let value: number | null
  export let fieldname: string

  interface Extras {
    unit?: string
  }

  export let extras: Extras = {}
</script>

<div class="flex items-center gap-4">
  <LowLevelDecimalField bind:value name={fieldname} unit={extras.unit} />
  <slot />
</div>
