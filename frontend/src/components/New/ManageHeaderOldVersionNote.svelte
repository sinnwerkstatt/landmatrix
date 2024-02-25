<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"

  export let obj: DealHull | InvestorHull

  $: isDeal = "fully_updated_at" in obj
  $: objType = isDeal ? "deal" : "investor"
  $: i18nValues = { values: { object: objType } }
</script>

{#if ![obj.active_version_id, obj.draft_version_id].includes(obj.selected_version.id)}
  <div
    class="my-4 rounded border border-orange-500 bg-orange-100 px-4 py-2 text-lg dark:bg-orange-800"
  >
    <span class="whitespace-nowrap">
      {$_("Please note: you are viewing an old version of this {object}.", i18nValues)}
    </span>

    <span class="whitespace-nowrap">
      {$_("The current version can be found here:")}
      <a href="/{objType}/{obj.id}/" class="text-pelorous hover:text-pelorous-300">
        {isDeal ? $_("Deal") : $_("Investor")} #{obj.id}
      </a>
    </span>
  </div>
{/if}
