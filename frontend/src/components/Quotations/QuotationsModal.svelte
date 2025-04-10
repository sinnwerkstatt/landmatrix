<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import type { DataSource, QuotationItem } from "$lib/types/data"

  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Modal from "$components/Modal.svelte"
  import SubmodelPopup from "$components/Quotations/SubmodelPopup.svelte"

  interface Props {
    open: boolean
    fieldname: string
    dataSources: DataSource[]
    quotes: QuotationItem[]
    setQuotes?: (quotations: QuotationItem[]) => void
  }

  let {
    open = $bindable(),
    fieldname,
    dataSources,
    quotes,
    setQuotes,
  }: Props = $props()

  let editable = $derived(!!setQuotes)

  const sortQuotes = (quotes: QuotationItem[]): QuotationItem[] => {
    const sortedNids = dataSources.map(ds => ds.nid)
    return quotes.toSorted(
      (a, b) => sortedNids.indexOf(a.nid) - sortedNids.indexOf(b.nid),
    )
  }

  const deleteQuotation = (i: number) => {
    const newQuotes = sortQuotes(quotes.filter((_, index) => index !== i))
    setQuotes?.(newQuotes)
  }

  let newQuotationId = $state<string | null>(
    dataSources.length > 0 ? dataSources[dataSources.length - 1].nid : null,
  )
  let newQuotationPages = $state("")

  const onsubmit = (event: SubmitEvent) => {
    event.preventDefault()

    if (newQuotationId) {
      const newQuotes = sortQuotes([
        ...quotes,
        { nid: newQuotationId, pages: newQuotationPages },
      ])
      setQuotes?.(newQuotes)

      newQuotationPages = ""
    }
  }

  const padLeadingZeros = (nDigits: number, value: number) => {
    return ("0".repeat(nDigits) + value.toString()).slice(-nDigits)
  }
</script>

<Modal
  class="h-full w-full px-4 py-8 lg:h-2/3 lg:w-2/3 lg:px-8 lg:py-12 dark:bg-gray-900"
  bind:open
  dismissible
>
  <div class="flex h-full w-full flex-col">
    <header class="mb-2 border-b border-gray-200">
      <h2 class="heading3">
        {$_("Linked data sources")}
      </h2>

      <span class="after:content-[':']">
        {$_("Field")}
      </span>
      <span class="italic">{fieldname}</span>
    </header>

    <ul class="grid grid-cols-1 gap-4 overflow-y-auto md:grid-cols-3 lg:grid-cols-4">
      {#each sortQuotes(quotes) as quote, i}
        {@const dsIndex = dataSources.findIndex(ds => ds.nid === quote.nid)}
        {@const dataSource = dataSources[dsIndex]}
        {@const label = `${padLeadingZeros(2, dsIndex + 1)}. ${$_("Data Source")}`}
        {@const href = new URL(`../data-sources/#${dataSource.nid}`, page.url.href)}

        <li
          class="flex gap-2 border border-black p-2 hover:bg-gray-50 dark:border-white hover:dark:bg-a-gray-800"
        >
          {#if dsIndex > -1}
            <div class="flex flex-grow flex-col">
              <span class="font-bold">{label}</span>

              <small class="text-sm text-gray-500">
                #{dataSource.nid}
              </small>

              <span class="text-nowrap italic text-gray-700 dark:text-gray-100">
                {$_("Page: {pages}", {
                  values: { pages: quote.pages ?? "--" },
                })}
              </span>
            </div>
            <a
              class="flex items-center text-purple-400 hover:text-purple-500"
              href={href.toString()}
              target="_blank"
            >
              <SubmodelPopup key="datasources" entry={dataSource} {label} />
            </a>
          {:else}
            <div class="font-bold text-red-400">
              {$_("Could not find data source: ") + `${quote.nid}`}
            </div>
          {/if}

          {#if editable}
            <button
              class="p-2 text-red-400"
              type="button"
              title={$_("Delete Quotation")}
              onclick={() => deleteQuotation(i)}
            >
              <TrashIcon />
            </button>
          {/if}
        </li>
      {:else}
        <li class="flex border border-black p-2 dark:border-white">
          {$_("No linked data sources yet.")}
        </li>
      {/each}
    </ul>

    {#if editable}
      <h2 class="heading4 mt-8">
        {$_("Create:")}
      </h2>

      <form class="mt-6 flex h-1/2 flex-col gap-4" {onsubmit}>
        <fieldset
          class="grid grid-cols-1 gap-4 overflow-y-auto md:grid-cols-3 lg:grid-cols-4"
        >
          <legend class="mb-2 inline-block">
            {$_("Select data source:")}
          </legend>

          {#each dataSources.toReversed() as dataSource, i}
            {@const index = dataSources.length - i - 1}
            {@const label = `${padLeadingZeros(2, index + 1)}. ${$_("Data Source")}`}

            <div
              class="flex text-left font-bold hover:bg-gray-50 hover:dark:bg-gray-800"
            >
              <input
                class="peer pointer-events-none fixed w-0 opacity-0"
                type="radio"
                id="{fieldname}-data-source-{dataSource.nid}"
                name="data-source-nid"
                bind:group={newQuotationId}
                value={dataSource.nid}
                required
              />
              <label
                class="inline-flex w-full cursor-pointer items-center justify-between border border-black peer-checked:bg-yellow dark:bg-gray-500 peer-checked:dark:text-black"
                for="{fieldname}-data-source-{dataSource.nid}"
              >
                <span class="p-2">
                  {label}
                </span>
                <SubmodelPopup key="datasources" entry={dataSource} {label} />
              </label>
            </div>
          {/each}
        </fieldset>

        <div class="flex items-center gap-2">
          <label for="page-number">
            {$_("Specify page in uploaded file (optional):")}
          </label>
          <input
            id="page-number"
            class="inpt w-fit outline-none"
            bind:value={newQuotationPages}
            placeholder="0"
          />
        </div>

        <div class="flex justify-between">
          <button class="btn btn-black" type="submit" disabled={!newQuotationId}>
            {$_("Add Quotation")}
          </button>
          <button class="btn btn-black" type="button" onclick={() => (open = false)}>
            {$_("Close")}
          </button>
        </div>
      </form>
    {:else}
      <div class="grow"></div>
      <div class="mt-2 flex justify-end">
        <button class="btn btn-black" type="button" onclick={() => (open = false)}>
          {$_("Close")}
        </button>
      </div>
    {/if}
  </div>
</Modal>
