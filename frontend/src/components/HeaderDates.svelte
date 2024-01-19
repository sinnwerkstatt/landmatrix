<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let obj: DealHull | InvestorHull
</script>

<div
  class="my-2 flex w-auto items-center whitespace-nowrap bg-gray-50 p-3 text-center text-gray-700 dark:bg-gray-700 dark:text-white"
>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Created")}
    <DisplayField fieldname="created_at" value={obj.selected_version.created_at} />
  </div>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Last update")}
    <DisplayField
      fieldname="modified_at"
      value={obj.selected_version.modified_at ?? obj.selected_version.created_at}
    />
  </div>
  {#if obj.fully_updated_at}
    <div class="mr-10 text-xs md:mx-5 md:text-sm">
      {$_("Last full update")}
      <DisplayField fieldname="fully_updated_at" value={obj.fully_updated_at} />
    </div>
  {/if}
</div>
