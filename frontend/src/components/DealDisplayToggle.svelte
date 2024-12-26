<script lang="ts">
  import { _ } from "svelte-i18n"

  import { displayDealsCount } from "$components/Map/mapHelper"

  let displayDeals = $derived(
    $displayDealsCount ? "bg-orange text-white" : "bg-white dark:bg-gray-800",
  )
  let displaySize = $derived(
    !$displayDealsCount ? "bg-orange text-white" : "bg-white dark:bg-gray-800",
  )
</script>

<div class="mt-8 flex justify-center text-center">
  <button
    type="button"
    onclick={() => displayDealsCount.set(true)}
    class="my-2 transform border px-3 py-2 font-bold duration-100 hover:underline {displayDeals}"
  >
    {$_("No. of deals")}
  </button>
  <button
    type="button"
    onclick={() => displayDealsCount.set(false)}
    class="my-2 transform border px-3 py-2 font-bold duration-100 hover:underline {displaySize}"
  >
    {$_("Deal size")}
  </button>
</div>
