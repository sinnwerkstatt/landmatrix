<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { datasourceChoices } from "$lib/fieldChoices"
  import type { DataSource, QuotationItem } from "$lib/types/data"

  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import Modal from "$components/Modal.svelte"
  import DSQuotationPopup from "$components/New/DSQuotationsPopup.svelte"

  interface Props {
    open: boolean
    fieldname: string
    quotes?: QuotationItem[]
    dataSources?: DataSource[]
    editable?: boolean
    label: string
  }

  let {
    open = $bindable(),
    quotes = $bindable(),
    dataSources = [],
    editable = false,
    fieldname,
    label,
  }: Props = $props()

  type PartialQuotationItem = Partial<QuotationItem>

  const createQuotation = (): PartialQuotationItem => ({
    nid: dataSources.length > 0 ? dataSources[dataSources.length - 1].nid : undefined,
  })

  const deleteQuotation = (i: number) => {
    if (quotes && i < quotes.length) {
      quotes = quotes.filter((_, index) => index !== i)
    }
  }

  let newQuotation: PartialQuotationItem = $state(createQuotation())

  const onsubmit = (event: SubmitEvent) => {
    event.preventDefault()

    if (!newQuotation.nid) {
      return
    }

    quotes = [...(quotes ?? []), $state.snapshot(newQuotation) as QuotationItem]

    newQuotation = createQuotation()
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
    <span class="font-bold italic">{label}</span>
    <hr class="mb-4" />

    <ul class="flex w-full flex-col gap-2">
      {#each quotes ?? [] as quote, i}
        {@const dsIndex = dataSources.findIndex(ds => ds.nid === quote.nid)}

        {#if dsIndex > -1}
          {@const ds = dataSources[dsIndex]}
          {@const dsTypeLabel = $datasourceChoices.type.find(
            entry => entry.value === ds.type,
          )?.label}

          <li
            class="flex border border-black p-2 hover:bg-gray-50 dark:border-white hover:dark:bg-a-gray-800"
          >
            <div class="w-max-[75%] flex flex-col">
              <div class="font-bold">
                <span>
                  {padLeadingZeros(2, dsIndex + 1)}. {$_("Data Source")}
                </span>
                <span>
                  ({dsTypeLabel})
                  {ds.name}
                </span>
                <a
                  class="mx-2 font-mono text-sm italic text-purple-400 hover:text-purple-500"
                  href="/deal/{page.data.dealID}/{page.data.dealVersion
                    ? page.data.dealVersion + '/'
                    : ''}data-sources/#{ds.nid}"
                  target="_blank"
                  rel="noreferrer"
                  title={$_("View Data Source")}
                >
                  #{ds.nid}
                </a>
              </div>

              <div class="flex gap-5">
                <span class="text-nowrap italic text-gray-700 dark:text-gray-100">
                  {$_("Page: {pageNumber}", {
                    values: { pageNumber: quote.page ?? "--" },
                  })}
                </span>
              </div>
            </div>

            <span class="flex-grow"></span>

            {#if editable}
              <button
                class="p-2 text-red-400 hover:text-red-500"
                type="button"
                title={$_("Delete Quotation")}
                onclick={() => deleteQuotation(i)}
              >
                <TrashIcon />
              </button>
            {/if}
          </li>
        {:else}
          <span class="color-red-400">
            {$_("Could not find data source.") + `${quote.nid}`}
          </span>
        {/if}
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
              <div
                class="flex justify-start gap-1 bg-gray-50 p-1 text-left font-bold dark:bg-gray-800"
              >
                <input
                  type="radio"
                  id="{fieldname}-data-source-{dataSource.nid}"
                  name="data-source-nid"
                  bind:group={newQuotation.nid}
                  value={dataSource.nid}
                />
                <label
                  class="inline-flex flex-grow cursor-pointer flex-col"
                  for="{fieldname}-data-source-{dataSource.nid}"
                >
                  {label}
                </label>
              </div>
            </DSQuotationPopup>
          {/each}
        </fieldset>
        <div>
          <label class="mb-2 inline-block" for="page-number">
            {$_("Specify page in uploaded file (optional):")}
          </label>
          <input
            id="page-number"
            class="inpt"
            bind:value={newQuotation.page}
            type="number"
            placeholder="0"
            min="0"
            max="999"
          />
        </div>

        <button class="btn btn-black" type="submit" disabled={!newQuotation.nid}>
          {$_("Add Quotation")}
        </button>
      </form>
    {/if}
  </div>
</Modal>
