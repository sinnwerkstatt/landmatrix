<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DataSource, QuotationItem } from "$lib/types/data"

  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Modal from "$components/Modal.svelte"
  import DSQuotationPopup from "$components/Quotations/DataSourcePopup.svelte"

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
  class="h-full w-full px-4 py-8 lg:h-fit lg:w-2/3 lg:px-8 lg:py-12 dark:bg-gray-900"
  bind:open
  dismissible
>
  <div>
    <h2 class="heading3">
      {$_("Linked data sources")}
    </h2>

    {$_("Field")}:
    <span class="font-bold italic">{fieldname}</span>
    <hr class="mb-4" />

    <ul class="grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-4">
      {#each sortQuotes(quotes) as quote, i}
        {@const dsIndex = dataSources.findIndex(ds => ds.nid === quote.nid)}

        <li
          class="flex gap-2 border border-black p-2 hover:bg-gray-50 dark:border-white hover:dark:bg-a-gray-800"
        >
          {#if dsIndex > -1}
            {@const ds = dataSources[dsIndex]}

            {@const label = `${padLeadingZeros(2, dsIndex + 1)}. ${$_("Data Source")}`}

            <div class="flex flex-grow flex-col">
              <DSQuotationPopup dataSource={ds} {label}>
                <div class="font-bold">
                  <span>
                    {padLeadingZeros(2, dsIndex + 1)}. {$_("Data Source")}
                  </span>
                </div>

                <div class="flex gap-5">
                  <span class="text-nowrap italic text-gray-700 dark:text-gray-100">
                    {$_("Page: {pages}", {
                      values: { pages: quote.pages ?? "--" },
                    })}
                  </span>
                </div>
              </DSQuotationPopup>
            </div>
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

      <form class="mt-6 flex flex-col gap-4" {onsubmit}>
        <fieldset class="grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-4">
          <legend class="mb-2 inline-block">
            {$_("Select data source:")}
          </legend>

          {#each dataSources as dataSource, i}
            {@const label = `${padLeadingZeros(2, i + 1)}. ${$_("Data Source")}`}

            <DSQuotationPopup {dataSource} {label}>
              <div class="text-left font-bold hover:bg-gray-50 hover:dark:bg-gray-800">
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
                  class="inline-block w-full cursor-pointer border border-black p-2
                   peer-checked:bg-yellow dark:bg-gray-500"
                  for="{fieldname}-data-source-{dataSource.nid}"
                >
                  {label}
                </label>
              </div>
            </DSQuotationPopup>
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
      <div class="mt-2 flex justify-end">
        <button class="btn btn-black" type="button" onclick={() => (open = false)}>
          {$_("Close")}
        </button>
      </div>
    {/if}
  </div>
</Modal>
