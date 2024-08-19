<script lang="ts">
  import type { InvestorDeal } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: InvestorDeal

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"

  const version_fields = [
    "current_intention_of_investment",
    "current_negotiation_status",
    "current_implementation_status",
    "deal_size",
  ] as const
</script>

<div class="flex flex-col gap-1 border border-orange p-2">
  <DisplayField
    fieldname="id"
    {labelClass}
    value={deal.id}
    {valueClass}
    {wrapperClass}
    showLabel
  />
  <DisplayField
    fieldname="country_id"
    {labelClass}
    value={deal.country_id}
    {valueClass}
    {wrapperClass}
    showLabel
  />

  {#each version_fields as fieldname}
    <DisplayField
      {fieldname}
      {labelClass}
      value={deal.selected_version[fieldname]}
      {valueClass}
      {wrapperClass}
      showLabel
    />
  {/each}
</div>
