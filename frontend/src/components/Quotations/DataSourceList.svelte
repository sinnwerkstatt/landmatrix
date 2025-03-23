<script lang="ts">
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import type { DataSource, QuotationItem, Quotations } from "$lib/types/data"
  // TODO: Refactor and use more specific helpers
  import { getQuotations, setAndCleanQuotations } from "$lib/utils/quotations"

  import {
    anySelected,
    getSelectedPaths,
  } from "$components/Quotations/selectedPaths.svelte"
  import SubmodelPopup from "$components/Quotations/SubmodelPopup.svelte"

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

<ul class="flex h-fit flex-col gap-2 overflow-y-scroll py-2">
  {#each dataSources.toReversed() as dataSource, i}
    {@const index = dataSources.length - i}
    {@const label = `${index}. ${$_("Data Source")}`}
    {@const isAny = isQuotedByAny(dataSource.nid)}
    {@const isAll = isQuotedByAll(dataSource.nid)}

    <li>
      <button
        class={twMerge(
          "group flex w-full items-center justify-between px-2 text-left",
          anySelected() && isAll
            ? "bg-yellow dark:text-black"
            : isAny
              ? "bg-yellow/20"
              : "bg-white dark:bg-gray-500",
        )}
        type="button"
        disabled={!anySelected()}
        title={!anySelected() ? $_("Select a change to attribute data source") : ""}
        onclick={() => onSelect(dataSource.nid)}
      >
        <span class="my-1 inline-flex flex-grow flex-col">
          {index}. {$_("Data Source")}
          <small class="text-white-500 text-sm">
            #{dataSource.nid}
          </small>
        </span>
        <SubmodelPopup key="datasources" entry={dataSource} {label} />
      </button>
    </li>
  {/each}
</ul>
