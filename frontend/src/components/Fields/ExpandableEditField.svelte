<script lang="ts">
  import { slide } from "svelte/transition"

  import type { Field } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import EditField from "$components/Fields/EditField.svelte"

  export let deal: Deal
  export let field: Field

  const isObject = (field: object | string): field is object =>
    typeof field === "object"

  $: fieldname = isObject(field) ? field.name : field
  $: isExpanded = isObject(field) ? deal[fieldname] === true : false
</script>

<EditField {fieldname} bind:value={deal[fieldname]} />

{#if isExpanded}
  <div transition:slide class="pl-4">
    {#each field.fields as nestedField}
      <svelte:self bind:deal field={nestedField} />
    {/each}
  </div>
{/if}
