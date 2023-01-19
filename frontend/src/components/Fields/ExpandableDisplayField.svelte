<script lang="ts">
  import type { Field } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: Deal
  export let field: Field

  $: fieldname = typeof field == "object" ? field.name : field
  $: isExpanded = typeof field === "object" ? deal[fieldname] === true : false
</script>

<DisplayField {fieldname} value={deal[fieldname]} showLabel />

{#if isExpanded}
  {#each field.fields as nestedField}
    <svelte:self {deal} field={nestedField} />
  {/each}
{/if}
