<script lang="ts" module>
  import type { Component } from "svelte"

  /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
  import type { Submodel } from "$lib/utils/dataProcessing"

  type ExtraProps<T> =
    T extends Component<infer Y extends Record<string, unknown>> ? Y["extras"] : never
</script>

<script lang="ts" generics="T extends Submodel, X extends Component<any, any, any>">
  import { onMount, type Snippet } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import { newNanoid } from "$lib/helpers"
  import type { Model } from "$lib/types/data"
  import { isEmptySubmodel, type SubmodelIdKeys } from "$lib/utils/dataProcessing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  import ConfirmSubmodelDeletionModal from "$components/ConfirmSubmodelDeletionModal.svelte"
  import { getMutableObject } from "$components/Data/stores"
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  interface Props {
    /* eslint-disable no-undef */
    model?: Model
    entries: T[]
    createEntry: (nid: string) => T
    entryComponent: X
    extras?: ExtraProps<X>
    filterFn?: (entry: T) => boolean
    isEmpty?: (entry: T) => boolean
    label: string
    selectedEntryId?: string | undefined // for external reference
    entryIdKey?: SubmodelIdKeys
    extraHeader?: Snippet<[T]>
    /* eslint-enable no-undef */
    onchange?: () => void
    isDataSource?: boolean
  }

  let {
    model = "deal",
    entries = $bindable(),
    createEntry,
    entryComponent,
    extras,
    filterFn = () => true,
    isEmpty = isEmptySubmodel,
    label,
    selectedEntryId = $bindable(),
    entryIdKey = "nid",
    extraHeader,
    onchange,
    isDataSource = false,
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

    const currentIDs = entries.map(entry => `${entry[entryIdKey]}`)
    const newEntryId = newNanoid(currentIDs)
    entries = [...entries, createEntry(newEntryId)]
    onchange?.()
    goto(`#${newEntryId}`)
  }

  const removeEntry = (id: string) => {
    const entry = entries.find(entry => `${entry[entryIdKey]}` === id)

    if (!entry) return

    entries = entries.filter(x => `${x[entryIdKey]}` !== id)

    if (isDataSource) {
      $mutableObj.selected_version.ds_quotations = Object.fromEntries(
        Object.entries($mutableObj.selected_version.ds_quotations)
          .map(([k, v]) => [k, v.filter(q => q.nid !== id)])
          // eslint-disable-next-line @typescript-eslint/no-unused-vars
          .filter(([_, v]) => !!v && v.length > 0),
      )
    }

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
</script>

<ConfirmSubmodelDeletionModal
  bind:open={showConfirmDeletionModal}
  onconfirm={() => removeEntry(toBeDeletedId)}
  submodelLabel={label}
  id={toBeDeletedId}
  {isDataSource}
/>

<section class="w-full">
  <div class="flex w-full flex-col gap-2">
    {#each entries.filter(filterFn) as entry, index (entry[entryIdKey])}
      {@const idAsString = `${entry[entryIdKey]}`}
      {@const isSelectedEntry = selectedEntryId === idAsString}

      <article id={idAsString}>
        <header
          class="flex items-center bg-gray-50 p-1 dark:bg-gray-700"
          class:animate-fadeToWhite={isSelectedEntry}
          class:dark:animate-fadeToGray={isSelectedEntry}
        >
          <h3 class="mb-0 flex-grow">
            <button
              aria-expanded={isSelectedEntry}
              aria-controls="form-{idAsString}"
              class="inline-flex w-full flex-row gap-1 text-left"
              type="button"
              onclick={() => toggleEntry(idAsString)}
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
                    #{idAsString}
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
                toBeDeletedId = idAsString
              } else {
                removeEntry(idAsString)
              }
            }}
            type="button"
          >
            <TrashIcon class="h-8 w-6 text-red-600" />
          </button>
        </header>

        <form id="form-{idAsString}">
          {#if isSelectedEntry}
            {@const SvelteComp = entryComponent}
            <div class="p-2" transition:slide={{ duration: 200 }}>
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
