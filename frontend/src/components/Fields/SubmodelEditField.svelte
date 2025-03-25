<script lang="ts" module>
  import type { Component } from "svelte"

  import type { SubmodelEntry } from "$lib/utils/dataProcessing"

  type ExtraProps<T> = T extends Component<infer Y> ? Y["extras"] : never

  /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
  type AnyComponent = Component<any, any, any>
</script>

<script lang="ts" generics="T extends SubmodelEntry, X extends AnyComponent">
  import { onMount, type Snippet } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import { type SubmodelFieldName } from "$lib/fieldLookups"
  import { newNanoid } from "$lib/helpers"
  import type {
    Model,
    QuotationItem,
    Quotations,
    SubmodelQuotations,
  } from "$lib/types/data"
  import { isEmptySubmodel } from "$lib/utils/dataProcessing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"
  import { removeAndCleanQuotations } from "$lib/utils/quotations"

  import ConfirmSubmodelDeletionModal from "$components/ConfirmSubmodelDeletionModal.svelte"
  import { getMutableObject } from "$components/Data/stores"
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"
  import SourcesEditButton from "$components/Quotations/SourcesEditButton.svelte"

  interface Props {
    model?: Model
    label: string
    fieldname: SubmodelFieldName
    entries: T[]
    createEntry: (nid: string) => T
    entryComponent: X
    extras?: ExtraProps<X>
    isEmpty?: (entry: T) => boolean
    selectedEntryId?: string | undefined // for external reference
    extraHeader?: Snippet<[T]>
    onchange?: () => void
  }

  let {
    model = "deal",
    label,
    fieldname,
    entries = $bindable(),
    createEntry,
    entryComponent,
    extras,
    isEmpty = isEmptySubmodel,
    selectedEntryId = $bindable(),
    extraHeader,
    onchange,
  }: Props = $props()

  $effect(() => {
    selectedEntryId = page.url.hash?.replace("#", "") || undefined
  })

  $effect(() => {
    scrollEntryIntoView(selectedEntryId)
  })

  onMount(() => scrollEntryIntoView(selectedEntryId))

  const mutableObj = getMutableObject(model)

  const addEntry = () => {
    if (selectedEntryForm && !selectedEntryForm.checkValidity()) {
      selectedEntryForm.reportValidity()
      return
    }

    const currentIDs = entries.map(entry => entry.nid)
    const newEntryId = newNanoid(currentIDs)
    entries = [...entries, createEntry(newEntryId)]
    onchange?.()
    goto(`#${newEntryId}`)
  }

  const removeEntry = (id: string | null) => {
    if (!id) return

    if (isDataSource) {
      // TODO: fix me
      $mutableObj.selected_version.ds_quotations = removeAndCleanQuotations(
        $mutableObj.selected_version.ds_quotations,
        id,
      ) as Quotations
    } else {
      setQuotes(id, [])
    }

    entries = entries.filter(x => x.nid !== id)

    showConfirmDeletionModal = false
    toBeDeletedId = null

    onchange?.()
    goto("")
  }

  let selectedEntryForm: HTMLFormElement | null = $derived(
    selectedEntryId
      ? (document.getElementById(`form-${selectedEntryId}`) as HTMLFormElement)
      : null,
  )

  const toggleEntry = (id: string): void => {
    if (selectedEntryForm && !selectedEntryForm.checkValidity()) {
      selectedEntryForm.reportValidity()
      return
    }

    goto(selectedEntryId === id ? "" : `#${id}`)
  }

  let showConfirmDeletionModal = $state(false)
  let toBeDeletedId: null | string = $state(null)

  let isDataSource = $derived(fieldname === "datasources")

  const getSubmodelQuotations = () =>
    ($mutableObj.selected_version.ds_quotations[fieldname] ?? {}) as SubmodelQuotations

  const getQuotes = (submodelNid: string): QuotationItem[] =>
    getSubmodelQuotations()[submodelNid] ?? []

  const setQuotes = (submodelNid: string, quotes: QuotationItem[]): void => {
    const { [submodelNid]: _ignore, ...rest } = getSubmodelQuotations()

    $mutableObj.selected_version.ds_quotations[fieldname] = quotes.length
      ? { ...rest, [submodelNid]: quotes }
      : rest

    if (!Object.keys(getSubmodelQuotations()).length) {
      const { [fieldname]: _ignore, ...rest } =
        $mutableObj.selected_version.ds_quotations ?? {}
      $mutableObj.selected_version.ds_quotations = { ...rest }
    }
  }
</script>

{#if toBeDeletedId}
  <ConfirmSubmodelDeletionModal
    bind:open={showConfirmDeletionModal}
    onconfirm={() => removeEntry(toBeDeletedId)}
    submodelLabel={label}
    id={toBeDeletedId}
    {isDataSource}
  />
{/if}

<section class="w-full">
  <div class="flex w-full flex-col gap-2">
    {#each entries as entry, index}
      {@const isSelectedEntry = selectedEntryId === entry.nid}

      <article id={entry.nid}>
        <header
          class="flex items-center bg-gray-50 p-1 dark:bg-gray-700"
          class:animate-fadeToWhite={isSelectedEntry}
          class:dark:animate-fadeToGray={isSelectedEntry}
        >
          <h3 class="mb-0 flex-grow">
            <button
              aria-expanded={isSelectedEntry}
              aria-controls="form-{entry.nid}"
              class="inline-flex w-full flex-row gap-1 text-left"
              type="button"
              onclick={() => toggleEntry(entry.nid)}
            >
              <span
                class="transition-duration-300 self-center p-2 transition-transform"
                class:rotate-180={isSelectedEntry}
              >
                <ChevronDownIcon class="h-4 w-4" />
              </span>
              <span class="inline-flex flex-col">
                <span>
                  <span class="heading4">
                    {index + 1}. {label}
                  </span>
                  <span class="font-mono text-sm text-gray-500">
                    #{entry.nid}
                  </span>
                </span>
                <span>
                  {@render extraHeader?.(entry)}
                </span>
              </span>
            </button>
          </h3>

          <button
            class="self-stretch p-2"
            onclick={() => {
              if (!isEmpty(entry)) {
                showConfirmDeletionModal = true
                toBeDeletedId = entry.nid
              } else {
                removeEntry(entry.nid)
              }
            }}
            type="button"
          >
            <TrashIcon class="h-8 w-6 text-red-600" />
          </button>
        </header>

        <form id="form-{entry.nid}">
          {#if isSelectedEntry}
            {@const SvelteComp = entryComponent}

            <div class="p-2" transition:slide={{ duration: 200 }}>
              {#if !isDataSource}
                <div class="my-2 ml-4">
                  <SourcesEditButton
                    fieldname="{fieldname}-{entry.nid}"
                    bind:quotes={
                      () => getQuotes(entry.nid), // force line break
                      quotes => setQuotes(entry.nid, quotes)
                    }
                    dataSources={$mutableObj.selected_version.datasources}
                  />
                </div>
              {/if}

              <SvelteComp bind:entry={entries[index]} {extras} {onchange} />
            </div>
          {/if}
        </form>
      </article>
    {:else}
      <form></form>
    {/each}
  </div>
  <!--  <div class="sticky bottom-0 z-[10] mt-6 w-full bg-white dark:bg-gray-900">-->
  <div class="mt-6">
    <button
      class="btn btn-flat btn-primary flex items-center"
      onclick={addEntry}
      type="button"
    >
      <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
      {$_("Add")}
      {label}
    </button>
  </div>
</section>
