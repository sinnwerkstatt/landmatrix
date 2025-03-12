<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import type { Model } from "$lib/types/data"

  import DSQuotationsModal from "$components/Quotations/QuotationsModal.svelte"

  interface Props {
    path: (string | number)[]
    model?: Model
  }

  let { path, model = "deal" }: Props = $props()

  let showDSQuotationModal = $state(false)

  let quotes = $derived.by(() => {
    let val = page.data[model]?.selected_version.ds_quotations ?? {}
    for (const p of path) {
      val = val?.[p]
    }
    return val ?? []
  })
  let dataSources = $derived(page.data[model]?.selected_version.datasources ?? [])
</script>

{#if quotes.length > 0}
  <button
    class="ml-4 italic text-purple-400 disabled:text-gray-500 dark:disabled:text-gray-100"
    type="button"
    onclick={() => {
      showDSQuotationModal = true
    }}
  >
    {$_("Sources")}: {quotes.length}
  </button>

  <DSQuotationsModal
    bind:open={showDSQuotationModal}
    fieldname={path.join("-")}
    {dataSources}
    {quotes}
  />
{/if}
