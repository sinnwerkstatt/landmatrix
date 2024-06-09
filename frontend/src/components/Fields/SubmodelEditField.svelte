<script lang="ts" context="module">
  /* eslint-disable @typescript-eslint/no-unused-vars */
  import type { SvelteComponent } from "svelte"

  import type { SubmodelEntry } from "$lib/utils/data_processing"

  /* eslint-enable @typescript-eslint/no-unused-vars */
</script>

<script
  lang="ts"
  generics="
  T extends SubmodelEntry,
  X extends typeof SvelteComponent<any>,
  Y extends Record<string, any>"
>
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { newNanoid } from "$lib/helpers"
  import { isEmptySubmodel } from "$lib/utils/data_processing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  /* eslint-disable no-undef */
  export let entries: T[]
  export let createEntry: (nid: string) => T
  export let entryComponent: X
  export let extras: Y
  /* eslint-enable no-undef */

  export let label: string

  let selectedEntryId: string | undefined
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

<section>
  <form class="w-full pb-52" id="{label}-entries">
    <div class="flex w-full flex-col gap-2">
      {#each entries as entry, index (entry.nid)}
        {@const isSelected = selectedEntryId === entry.nid}

        <div class="flex items-center bg-gray-50 px-2 dark:bg-gray-700">
          <h3 class="heading4 mb-0 flex-grow">
            {#if isSelected}
              <a href="">
                {index + 1}. {label}
                <small class="text-sm text-gray-500">
                  #{entry.nid}
                </small>
              </a>
            {:else}
              <a href="#{entry.nid}">
                {index + 1}. {label}
                <small class="text-sm text-gray-500">
                  #{entry.nid}
                </small>
              </a>
            {/if}
          </h3>
          <button
            class="flex-initial p-2"
            on:click|preventDefault={() => removeEntry(index)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if isSelected}
          <div transition:slide={{ duration: 200 }}>
            <svelte:component this={entryComponent} bind:entry {extras} />
          </div>
        {/if}
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
  </form>
</section>
