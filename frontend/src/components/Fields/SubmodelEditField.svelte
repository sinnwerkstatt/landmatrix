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
  import { goto } from "$app/navigation"
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
  export let filterFn: (entry: T) => boolean = () => true
  export let isEmpty: (entry: T) => boolean = isEmptySubmodel
  /* eslint-enable no-undef */
  export let label: string
  export let selectedEntryId: string | undefined = undefined // for external reference
  export let entryIdKey: "id" | "nid" = "nid"

  $: selectedEntryId = $page.url.hash?.replace("#", "") || undefined

  $: browser && scrollEntryIntoView(selectedEntryId)

  onMount(() => scrollEntryIntoView(selectedEntryId))

  const addEntry = () => {
    const currentIDs = entries.map(entry => `${entry[entryIdKey]}`)
    const newEntryId = newNanoid(currentIDs)
    entries = [...entries, createEntry(newEntryId)]
    goto(`#${newEntryId}`)
  }

  const removeEntry = (index: number) => {
    const entry = entries[index]

    if (!isEmpty(entry)) {
      const areYouSure = confirm(`${$_("Remove")} ${label} #${entry[entryIdKey]}}?`)
      if (!areYouSure) return
    }
    entries = entries.filter(x => `${x[entryIdKey]}` !== `${entry[entryIdKey]}`)
  }
</script>

<section class="w-full pb-52">
  <div class="flex w-full flex-col gap-2">
    {#each entries.filter(filterFn) as entry, index (entry[entryIdKey])}
      {@const isSelectedEntry = selectedEntryId === `${entry[entryIdKey]}`}

      <article id={`${entry[entryIdKey]}`}>
        <div
          class="flex items-center bg-gray-50 px-2 dark:bg-gray-700 {isSelectedEntry
            ? 'animate-fadeToWhite dark:animate-fadeToGray'
            : ''}"
        >
          <h3 class="heading4 mb-0 flex-grow">
            <button
              class="w-full text-left"
              on:click|preventDefault={() =>
                (window.location.hash = isSelectedEntry ? "" : `${entry[entryIdKey]}`)}
            >
              <ChevronDownIcon
                class="transition-duration-300 inline h-4 w-4 rounded transition-transform {isSelectedEntry
                  ? 'rotate-180'
                  : ''}"
              />
              {index + 1}. {label}
              <small class="text-sm text-gray-500">
                #{entry[entryIdKey]}
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
        <form id="{label}-entry-{entry[entryIdKey]}">
          {#if isSelectedEntry}
            <div class="p-2" transition:slide={{ duration: 200 }}>
              <svelte:component this={entryComponent} bind:entry {extras} />
            </div>
          {/if}
        </form>
      </article>
    {:else}
      <form></form>
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
