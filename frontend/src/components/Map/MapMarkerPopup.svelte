<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, Location2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: DealHull
  export let location: Location2

  const labelClass = "font-semibold"
  const valueClass = ""
  const wrapperClass = "mb-4"
</script>

<div class="heading4">{$_("Deal")} #{deal.id}</div>
<div class="deal-summary">
  <DisplayField
    fieldname="location.level_of_accuracy"
    {labelClass}
    showLabel
    value={location.level_of_accuracy}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="current_intention_of_investment"
    {labelClass}
    showLabel
    value={deal.selected_version.current_intention_of_investment}
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
  <DisplayField
    fieldname="operating_company"
    {labelClass}
    showLabel
    value={deal.selected_version.operating_company}
    {valueClass}
    {wrapperClass}
  />
</div>
<a class="btn btn-primary !text-white" href="/deal/{deal.id}/">
  {$_("More details")}
</a>
