<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { DealHull, Location2 } from "$lib/types/newtypes"

  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import InvestorLinkField from "$components/Fields/Display2/InvestorLinkField.svelte"
  import IOIField from "$components/Fields/Display2/IOIField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let deal: DealHull
  export let location: Location2

  const labelClass = "font-semibold"
  const valueClass = ""
  const wrapperClass = "mb-4"
</script>

<div class="heading4">{$_("Deal")} #{deal.id}</div>
<div class="deal-summary">
  <TextField
    label={$_("Spatial accuracy level")}
    value={location.level_of_accuracy}
    fieldname="location.level_of_accuracy"
    choices={$fieldChoices.deal.level_of_accuracy}
    {labelClass}
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
  <DecimalField
    value={deal.selected_version.deal_size}
    fieldname="deal_size"
    unit={$_("ha")}
    label={$_("Deal size")}
    {labelClass}
    {valueClass}
    {wrapperClass}
  />
  <InvestorLinkField
    fieldname="operating_company"
    label={$_("Operating Company")}
    value={deal.selected_version.operating_company}
    {labelClass}
    {valueClass}
    {wrapperClass}
  />
</div>
<a href="/deal/{deal.id}/" class="btn btn-primary !text-white">
  {$_("More details")}
</a>
