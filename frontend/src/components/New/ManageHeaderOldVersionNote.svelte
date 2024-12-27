<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/data"

  interface Props {
    obj: DealHull | InvestorHull
  }

  let { obj }: Props = $props()

  let isDeal = $derived("fully_updated_at" in obj)
  let objType = $derived(isDeal ? "deal" : "investor")
  let i18nValues = $derived({ values: { object: objType } })
</script>

{#if ![obj.active_version_id, obj.draft_version_id].includes(obj.selected_version.id)}
  <div
    class="my-4 rounded border border-orange-500 bg-orange-100 px-4 py-2 text-lg dark:bg-orange-800"
  >
    <span class="md:whitespace-nowrap">
      {$_("Please note: you are viewing an old version of this {object}.", i18nValues)}
    </span>

    <span class="md:whitespace-nowrap">
      {$_("The current version can be found here:")}
      <a href="/{objType}/{obj.id}/" class="text-pelorous hover:text-pelorous-300">
        {isDeal ? $_("Deal") : $_("Investor")} #{obj.id}
      </a>
    </span>
  </div>
{/if}
