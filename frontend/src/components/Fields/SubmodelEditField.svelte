<script lang="ts" context="module">
  /* eslint-disable @typescript-eslint/no-unused-vars */
  import type { SvelteComponent } from "svelte"

  import type { SubmodelEntry } from "$lib/utils/data_processing"

  /* eslint-enable @typescript-eslint/no-unused-vars */
</script>

<script
  lang="ts"
  generics="T extends SubmodelEntry, X extends typeof SvelteComponent<any>"
>
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  /* eslint-disable no-undef */
  export let entries: T[]
  export let createEntry: (nid: string) => T
  export let entryComponent: X
  /* eslint-enable no-undef */

  export let label: string

  let activeEntryIdx = -1

  const addEntry = () => {
    const currentIDs = entries.map(entry => entry.nid)
    entries = [...entries, createEntry(newNanoid(currentIDs))]
    activeEntryIdx = entries.length - 1
  }

  const removeEntry = (index: number) => {
    const entry = entries[index]

    if (!isEmptySubmodel(entry)) {
      console.log("inside remove", entry, isEmptySubmodel(entry))
      const areYouSure = confirm(`${$_("Remove")} ${label} #${entry.nid}}?`)
      if (!areYouSure) return
    }
    entries = entries.filter(x => x.nid !== entry.nid)
  }

  const toggleActiveEntry = (index: number) =>
    (activeEntryIdx = activeEntryIdx === index ? -1 : index)
</script>

<section class="flex flex-wrap">
  <form class="w-full pb-52" id="{label}-entries">
    {#each entries as entry, index (entry.nid)}
      <div>
        <div
          class="my-2 flex flex-row items-center justify-between bg-gray-200 dark:bg-gray-700"
        >
          <div
            role="button"
            class="flex-grow p-2"
            on:click={() => toggleActiveEntry(index)}
            on:keydown={e => e.code === "Enter" && toggleActiveEntry(index)}
            tabindex="0"
          >
            <h3 class="m-0">
              {index + 1}. {label}
              <small class="text-sm text-gray-500">
                #{entry.nid}
              </small>
            </h3>
          </div>
          <button
            class="flex-initial p-2"
            on:click|preventDefault={() => removeEntry(index)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if activeEntryIdx === index}
          <div transition:slide={{ duration: 200 }}>
            <svelte:component this={entryComponent} bind:entry />
          </div>
        {/if}
      </div>
    {/each}
    <div class="mt-6">
      <button
        class="btn btn-primary flex items-center"
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
