<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DataSource, QuotationItem, Quotations } from "$lib/types/data"
  // TODO: Refactor and use more specific helpers
  import { getQuotations, setAndCleanQuotations } from "$lib/utils/quotations"

  import DSQuotationsPopup from "$components/Quotations/DataSourcePopup.svelte"
  import {
    anySelected,
    getSelectedPaths,
  } from "$components/Quotations/selectedPaths.svelte"

  interface Props {
    dataSources: DataSource[]
    quotations: Quotations
  }

  let { dataSources, quotations = $bindable() }: Props = $props()

  const doesQuoteDataSource =
    (nid: string) =>
    (path: string[]): boolean => {
      const quotes = getQuotations(quotations, path) as QuotationItem[]
      return quotes.map(q => q.nid).includes(nid)
    }

  const isQuotedByAny = (nid: string): boolean =>
    getSelectedPaths().some(doesQuoteDataSource(nid))

  const isQuotedByAll = (nid: string): boolean =>
    getSelectedPaths().every(doesQuoteDataSource(nid))

  const sortQuotes = (quotes: QuotationItem[]): QuotationItem[] => {
    const sortedNids = dataSources.map(ds => ds.nid)
    return quotes.toSorted(
      (a, b) => sortedNids.indexOf(a.nid) - sortedNids.indexOf(b.nid),
    )
  }

  const onSelect = (nid: string): void => {
    if (isQuotedByAny(nid)) {
      getSelectedPaths().forEach(path => {
        const quotes = (getQuotations(quotations, path) as QuotationItem[]).filter(
          q => q.nid !== nid,
        )
        quotations = setAndCleanQuotations(quotations, path, quotes) as Quotations
      })
    } else {
      getSelectedPaths().forEach(path => {
        const quotes = sortQuotes([
          ...(getQuotations(quotations, path) as QuotationItem[]),
          { nid },
        ])
        quotations = setAndCleanQuotations(quotations, path, quotes) as Quotations
      })
    }
  }
</script>

<ol class="flex flex-col gap-2">
  {#each dataSources as dataSource, i}
    {@const label = `${i + 1}. ${$_("Data Source")}`}
    {@const isAny = isQuotedByAny(dataSource.nid)}
    {@const isAll = isQuotedByAll(dataSource.nid)}

    <li>
      <DSQuotationsPopup {dataSource} {label}>
        <button
          class="w-full p-2 text-left {anySelected() && isAll
            ? 'bg-yellow'
            : isAny
              ? 'bg-yellow/20'
              : 'bg-white dark:bg-gray-500'}"
          type="button"
          disabled={!anySelected()}
          onclick={() => onSelect(dataSource.nid)}
        >
          {i + 1}. {dataSource.nid}
        </button>
      </DSQuotationsPopup>
    </li>
  {/each}
</ol>
