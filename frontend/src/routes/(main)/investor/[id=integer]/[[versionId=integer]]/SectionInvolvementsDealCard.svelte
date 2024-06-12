<script lang="ts">
  import type { DealHull } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: DealHull

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"

  const fields = [
    "id",
    "country_id",
    "current_intention_of_investment",
    "current_negotiation_status",
    "current_implementation_status",
    "deal_size",
  ]
</script>

<div class="flex flex-col gap-1 border border-orange p-2">
  {#each fields as fieldname}
    {#if ["id", "country_id"].includes(fieldname)}
      <DisplayField
        {fieldname}
        {labelClass}
        value={deal[fieldname]}
        {valueClass}
        {wrapperClass}
        showLabel
      />
    {:else}
      <DisplayField
        {fieldname}
        {labelClass}
        value={deal.selected_version[fieldname]}
        {valueClass}
        {wrapperClass}
        showLabel
      />
    {/if}
  {/each}
</div>
