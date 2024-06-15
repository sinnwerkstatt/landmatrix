<script lang="ts">
  import type { DealHull, InvestorHull } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let obj: DealHull | InvestorHull
  const wrapperClass = "flex-col flex items-center"
  const valueClass = "text-base md:text-lg"
  const labelClass = "text-xs md:text-sm"
</script>

<div
  class="my-2 flex items-center justify-evenly gap-3 whitespace-nowrap bg-gray-50 p-3 text-gray-700 md:gap-5 dark:bg-gray-700 dark:text-white"
>
  <DisplayField
    fieldname="created_at"
    {labelClass}
    showLabel
    value={obj.first_created_at}
    {valueClass}
    {wrapperClass}
  />
  <DisplayField
    fieldname="modified_at"
    {labelClass}
    showLabel
    value={obj.selected_version.modified_at ?? obj.selected_version.created_at}
    {valueClass}
    {wrapperClass}
  />
  {#if "fully_updated_at" in obj}
    <DisplayField
      fieldname="fully_updated_at"
      value={obj.fully_updated_at}
      {wrapperClass}
      {valueClass}
      {labelClass}
      showLabel
    />
  {/if}
</div>
