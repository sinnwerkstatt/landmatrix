<script lang="ts">
  import { slide } from "svelte/transition"

  import type { Field } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import EditField from "$components/Fields/EditField.svelte"

  export let deal: Deal
  export let field: Field

  $: fieldname = typeof field == "object" ? field.name : field
  $: isExpanded = typeof field === "object" ? deal[fieldname] === true : false
</script>

<EditField {fieldname} bind:value={deal[fieldname]} />

{#if isExpanded}
  <div transition:slide class="pl-4">
    {#each field.fields as nestedField}
      <svelte:self bind:deal field={nestedField} />
    {/each}
  </div>
{/if}
