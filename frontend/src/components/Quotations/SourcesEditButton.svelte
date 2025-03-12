<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DataSource, QuotationItem } from "$lib/types/data"

  import DSQuotationsModal from "$components/Quotations/QuotationsModal.svelte"

  interface Props {
    fieldname: string
    quotes: QuotationItem[]
    dataSources?: DataSource[]
    disabled?: boolean
  }

  let {
    fieldname,
    quotes = $bindable(),
    dataSources = [],
    disabled = false,
  }: Props = $props()

  let showDSQuotationModal = $state(false)

  const setQuotes = (_quotes: QuotationItem[]): void => {
    quotes = _quotes
  }
</script>

<button
  class="italic text-purple-400 disabled:text-gray-500 dark:disabled:text-gray-100"
  type="button"
  onclick={() => {
    showDSQuotationModal = true
  }}
  {disabled}
>
  {$_("Sources")}: {quotes.length}
</button>

<DSQuotationsModal
  bind:open={showDSQuotationModal}
  {fieldname}
  {dataSources}
  {quotes}
  {setQuotes}
/>
