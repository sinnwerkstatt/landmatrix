<script lang="ts">
  import type { DealHull } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: DealHull

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"
</script>

<div class="flex flex-col gap-1 border border-orange p-2">
  <DisplayField
    fieldname="id"
    {labelClass}
    value={deal.id}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="country"
    {labelClass}
    value={deal.country_id}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="current_intention_of_investment"
    {labelClass}
    value={deal.selected_version.current_intention_of_investment}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="current_negotiation_status"
    {labelClass}
    showLabel
    value={deal.selected_version.current_negotiation_status}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="current_implementation_status"
    {labelClass}
    showLabel
    value={deal.selected_version.current_implementation_status}
    {valueClass}
    {wrapperClass}
  />

  <DisplayField
    fieldname="deal_size"
    {labelClass}
    showLabel
    value={deal.selected_version.deal_size}
    {valueClass}
    {wrapperClass}
  />
</div>
