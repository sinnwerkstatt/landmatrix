<script lang="ts">
  import { _ } from "svelte-i18n";
  import { displayDealsCount } from "$components/Map/map_helper";

  $: displayDeals = $displayDealsCount ? "bg-orange text-white" : "bg-white";
  $: displaySize = !$displayDealsCount ? "bg-orange text-white" : "bg-white";
</script>

<div class="text-center flex justify-center mt-8">
  <button
    type="button"
    on:click={() => displayDealsCount.set(true)}
    class="font-bold hover:underline my-2 py-2 px-3 transform duration-100 border {displayDeals}"
  >
    {$_("No. of deals")}
  </button>
  <button
    type="button"
    on:click={() => displayDealsCount.set(false)}
    class="font-bold hover:underline my-2 py-2 px-3 transform duration-100 border {displaySize}"
  >
    {$_("Deal size")}
  </button>
</div>
