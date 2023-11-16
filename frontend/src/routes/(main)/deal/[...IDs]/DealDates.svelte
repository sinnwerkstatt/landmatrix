<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"

  export let deal: DealHull
</script>

<div
  class="my-2 flex w-auto items-center bg-lm-lightgray p-3 text-center text-lm-dark dark:bg-gray-700 dark:text-white"
>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Created")}
    <br />
    <DateTimeField value={deal.created_at} />
  </div>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Last update")}
    <br />
    <DateTimeField value={deal.selected_version.activated_at} />
  </div>
  <div class="mr-10 text-xs md:mx-5 md:text-sm">
    {$_("Last full update")}
    <br />
    <DateTimeField value={deal.fully_updated_at} />
  </div>
</div>
