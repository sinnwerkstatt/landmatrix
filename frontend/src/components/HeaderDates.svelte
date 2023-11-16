<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes"

  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"

  export let obj: DealHull | InvestorHull
</script>

<div
  class="my-2 flex w-auto items-center bg-lm-lightgray p-3 text-center text-lm-dark dark:bg-gray-700 dark:text-white"
>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Created")}
    <br />
    <DateTimeField value={obj.created_at} />
  </div>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Last update")}
    <br />
    <DateTimeField value={obj.selected_version.activated_at} />
  </div>
  {#if obj.fully_updated_at}
    <div class="mr-10 text-xs md:mx-5 md:text-sm">
      {$_("Last full update")}
      <br />
      <DateTimeField value={obj.fully_updated_at} />
    </div>
  {/if}
</div>
