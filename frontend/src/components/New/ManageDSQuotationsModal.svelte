<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import type { components } from "$lib/openAPI"
  import type { Model } from "$lib/types/data"

  import IconTrashcan from "$components/Accountability/icons/IconTrashcan.svelte"
  import { mutableDeal, mutableInvestor } from "$components/Data/stores"
  import Modal from "$components/Modal.svelte"

  interface Props {
    open: boolean
    model: Model
    fieldname: string
    label: string
  }

  let { open = $bindable(), model = "deal", fieldname, label }: Props = $props()

  let mutableObj = $derived(model === "deal" ? $mutableDeal : $mutableInvestor)
  let dataSources = $derived(mutableObj.selected_version.datasources)
  let quotes: QuotationItem[] = $derived(
    mutableObj.selected_version.ds_quotations[fieldname] ?? [],
  )
  // let sortedQuotes: QuotationItem[] = $derived(
  //   quotes.toSorted((a, b) => {
  //     return (
  //       dataSources.findIndex(ds => ds.nid === a.nid) -
  //       dataSources.findIndex(ds => ds.nid === b.nid)
  //     )
  //   }),
  // )

  type QuotationItem = components["schemas"]["QuotationItem"]
  type PartialQuotationItem = Partial<QuotationItem>

  const createQuotation = (): PartialQuotationItem => ({})
  const deleteQuotation = (i: number) => {
    if (i < quotes.length) {
      mutableObj.selected_version.ds_quotations[fieldname] = quotes.filter(
        (_, index) => index !== i,
      )
    }
  }

  let newQuotation: PartialQuotationItem = $state(createQuotation())

  const onsubmit = (event: SubmitEvent) => {
    event.preventDefault()
    console.log($state.snapshot(newQuotation))

    if (!newQuotation.nid) {
      return
    }

    mutableObj.selected_version.ds_quotations[fieldname] = [
      ...quotes,
      $state.snapshot(newQuotation),
    ]

    newQuotation = createQuotation()
  }

  const padLeadingZeros = (nDigits: number, value: number) => {
    return ("0".repeat(nDigits) + value.toString()).slice(-nDigits)
  }
</script>

<Modal class="w-2/3 p-8 dark:bg-gray-900" bind:open dismissible>
  <div>
    <h2 class="heading3">
      {$_("Manage quotations")}
    </h2>

    {$_("Field")}:
    <span class="font-bold italic">{label}</span>
    <hr class="mb-4" />

    <ul class="flex w-full flex-col gap-2">
      {#each quotes as quote, i}
        {@const dsIndex = dataSources.findIndex(ds => ds.nid === quote.nid)}

        {#if dsIndex > -1}
          {@const ds = dataSources[dsIndex]}

          <li
            class="flex border border-black p-2 hover:bg-gray-50 dark:border-white hover:dark:bg-a-gray-800"
          >
            <div class="w-max-[75%] flex flex-col">
              <div class="font-bold">
                <span>
                  {padLeadingZeros(2, dsIndex + 1)}. {$_("Data Source")}
                </span>

                <a
                  class="mx-2 font-mono text-sm italic text-purple-400 hover:text-purple-500"
                  href={new URL("../data-sources/#" + ds.nid, page.url).href}
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

                <span
                  class="line-clamp-1 text-ellipsis italic text-gray-700 dark:text-gray-100"
                  title={quote.comment}
                >
                  {$_("Comment:")}
                  {@html quote.comment ?? "--"}
                </span>
              </div>
            </div>

            <span class="flex-grow"></span>

            <button
              class="p-2 text-red-400 hover:text-red-500"
              type="button"
              title={$_("Delete Quotation")}
              onclick={() => deleteQuotation(i)}
            >
              <IconTrashcan />
            </button>
          </li>
        {:else}
          <span class="color-red-400">
            {$_("Could not find data source") + `${quote.nid}`}
          </span>
        {/if}
      {:else}
        <li class="flex border border-black p-2 dark:border-white">
          {$_("No quotations yet")}
        </li>
      {/each}
    </ul>

    <h2 class="heading4 mt-8">
      {$_("New quotation:")}
    </h2>
    <form class="mt-6 flex flex-col gap-4" {onsubmit}>
      <fieldset class="flex flex-wrap gap-x-10 gap-y-2">
        <legend class="mb-2 inline-block">
          {$_("Select data source:")}
        </legend>

        {#each dataSources as dataSource, i}
          <div class="font-bold">
            <input
              type="radio"
              id="data-source-{dataSource.nid}"
              name="data-source-nid"
              bind:group={newQuotation.nid}
              value={dataSource.nid}
            />
            <label for="data-source-{dataSource.nid}">
              {padLeadingZeros(2, i + 1)}. {$_("Data Source")}
              <a
                class="mx-2 font-mono text-sm italic text-purple-400 hover:text-purple-500"
                href={new URL("../data-sources/#" + dataSource.nid, page.url).href}
                target="_blank"
                rel="noreferrer"
                title={$_("View Data Source")}
              >
                #{dataSource.nid}
              </a>
            </label>
          </div>
        {/each}
      </fieldset>

      <div>
        <label class="mb-2 inline-block" for="page-number">
          {$_("Choose page (optional):")}
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

      <div>
        <label class="mb-2 inline-block" for="comment">
          {$_("Add comment (optional):")}
        </label>
        <textarea
          class="inpt"
          id="comment"
          bind:value={newQuotation.comment}
          placeholder="comment"
        ></textarea>
      </div>

      <button class="btn btn-black" type="submit" disabled={!newQuotation.nid}>
        {$_("Add Quotation")}
      </button>
    </form>
  </div>
</Modal>
