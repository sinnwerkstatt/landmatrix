<script lang="ts" context="module">
  import type { SvelteComponent } from "svelte"

  /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
  import type { SubmodelEntry } from "$lib/utils/data_processing"

  type ExtraProps<T> = T extends typeof SvelteComponent<
    infer Y extends Record<string, unknown>
  >
    ? Y["extras"]
    : never
</script>

<script
  lang="ts"
  generics="
  T extends SubmodelEntry,
  X extends typeof SvelteComponent<any>,
"
>
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { newNanoid } from "$lib/helpers"
  import { isEmptySubmodel } from "$lib/utils/data_processing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  /* eslint-disable no-undef */
  export let entries: T[]
  export let createEntry: (nid: string) => T
  export let entryComponent: X
  export let extras: ExtraProps<X>
  /* eslint-enable no-undef */
  export let label: string
  export let selectedEntryId: string | undefined = undefined // for external reference

  $: selectedEntryId = $page.url.hash?.replace("#", "")

  $: browser && scrollEntryIntoView(selectedEntryId)

  onMount(() => scrollEntryIntoView(selectedEntryId))

  const addEntry = () => {
    const currentIDs = entries.map(entry => entry.nid)
    const newEntryId = newNanoid(currentIDs)
    entries = [...entries, createEntry(newEntryId)]
    selectedEntryId = newEntryId
  }

  const removeEntry = (index: number) => {
    const entry = entries[index]

    if (!isEmptySubmodel(entry)) {
      const areYouSure = confirm(`${$_("Remove")} ${label} #${entry.nid}}?`)
      if (!areYouSure) return
    }
    entries = entries.filter(x => x.nid !== entry.nid)
  }
</script>

<section class="w-full pb-52">
  <div class="flex w-full flex-col gap-2">
    {#each entries as entry, index (entry.nid)}
      {@const isSelectedEntry = selectedEntryId === entry.nid}

      <article id={entry.nid}>
        <div
          class="flex items-center bg-gray-50 px-2 dark:bg-gray-700 {isSelectedEntry
            ? 'animate-fadeToWhite dark:animate-fadeToGray'
            : ''}"
        >
          <h3 class="heading4 mb-0 flex-grow">
            <button
              class="w-full text-left"
              on:click|preventDefault={() =>
                (window.location.hash = isSelectedEntry ? "" : entry.nid)}
            >
              <ChevronDownIcon
                class="transition-duration-300 inline h-4 w-4 rounded transition-transform {isSelectedEntry
                  ? 'rotate-180'
                  : ''}"
              />
              {index + 1}. {label}
              <small class="text-sm text-gray-500">
                #{entry.nid}
              </small>
            </button>
          </h3>
          <button
            class="flex-initial p-2"
            on:click|preventDefault={() => removeEntry(index)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        <form id="{label}-entry-{entry.nid}">
          {#if isSelectedEntry}
            <div class="p-2" transition:slide={{ duration: 200 }}>
              <svelte:component this={entryComponent} bind:entry {extras} />
            </div>
          {/if}
        </form>
      </article>
    {/each}
  </div>
  <div class="mt-6">
    <button
      class="btn btn-flat btn-primary flex items-center"
      on:click={addEntry}
      type="button"
    >
      <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
      {$_("Add")}
      {label}
    </button>
  </div>
</section>
