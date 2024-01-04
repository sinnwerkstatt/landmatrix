<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { DealHull } from "$lib/types/newtypes"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import IDField from "$components/Fields/Display2/IDField.svelte"
  import IOIField from "$components/Fields/Display2/IOIField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let deal: DealHull

  const wrapperClass = "my-1 flex flex-wrap justify-between"
  const labelClass = "whitespace-nowrap font-light text-gray-400 pr-2 italic"
  const valueClass = "font-medium"
</script>

<div class="flex flex-col gap-1 border border-orange p-2">
  <IDField
    fieldname="deal.id"
    label={$_("ID")}
    {labelClass}
    value={deal.id}
    {valueClass}
    {wrapperClass}
  />
  <CountryField
    fieldname="country"
    label={$_("Target country")}
    {labelClass}
    value={deal.country}
    {valueClass}
    {wrapperClass}
  />
  <IOIField
    value={deal.selected_version.current_intention_of_investment}
    {labelClass}
    {valueClass}
    {wrapperClass}
    label={$_("Intention of investment")}
  />
  <!--            <TextField-->
  <!--
  <!--              -->
  <!--              fieldname="current_intention_of_investment"-->
  <!--              choices={$fieldChoices.deal.intention_of_investment}-->
  <!--            />-->
  <TextField
    choices={$fieldChoices.deal.negotiation_status}
    fieldname="current_negotiation_status"
    label={$_("Current negotiation status")}
    value={deal.selected_version.current_negotiation_status}
    {labelClass}
    {valueClass}
    {wrapperClass}
  />
  <TextField
    choices={$fieldChoices.deal.implementation_status}
    fieldname="current_implementation_status"
    label={$_("Current implementation status")}
    value={deal.selected_version.current_implementation_status}
    {labelClass}
    {valueClass}
    {wrapperClass}
  />

  <DecimalField
    value={deal.selected_version.deal_size}
    fieldname="deal_size"
    unit={$_("ha")}
    label={$_("Deal size")}
    {labelClass}
    {valueClass}
    {wrapperClass}
  />
</div>
