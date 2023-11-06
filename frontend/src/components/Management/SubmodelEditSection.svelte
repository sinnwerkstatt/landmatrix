<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { subsections } from "$lib/sections"
  import type { Contract, DataSource } from "$lib/types/deal"
  import type { Involvement } from "$lib/types/investor"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import EditField from "$components/Fields/EditField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  type Entry = Contract | DataSource | Involvement

  export let model: "datasource" | "contract" | "involvement"
  export let modelName: string
  export let entries: Entry[]
  export let entriesFilter: (i: Involvement) => boolean = () => true
  export let newEntryExtras = {}
  export let id: string

  export let fields = subsections[model]

  let activeEntry = -1

  // ensure entries is not null
  $: entries = entries ?? []
  // ensure entries to have non-null ids
  // new involvements have null ids when investor still in draft mode
  $: entries = createTempIdsIfNull(entries)

  const createTempIdsIfNull = (entries: Entry[]) =>
    entries.reduce((acc: Entry[], val: Entry): Entry[] => {
      const existingIds = acc.map(entry => entry.id.toString())
      return [...acc, { ...val, id: val.id ?? newNanoid(existingIds) } as Entry]
    }, [])

  function addEntry() {
    const currentIDs = entries.map(entry => entry.id.toString())
    const newEntry: Entry = { id: newNanoid(currentIDs), ...newEntryExtras }
    entries = [...entries, newEntry]
    activeEntry = entries.length - 1
  }

  function removeEntry(entry: Entry) {
    if (!isEmptySubmodel(entry)) {
      const areYouSure = confirm(
        `${$_("Remove")} ${modelName} ${getDisplayLabel(entry)}?`,
      )
      if (!areYouSure) return
    }

    entries = entries.filter(x => x.id !== entry.id)
  }
  function toggleActiveEntry(index: number): void {
    activeEntry = activeEntry === index ? -1 : index
  }

  const getDisplayLabel = (entry: Entry): string => {
    if (model == "involvement") {
      const investor = (entry as Involvement).investor
      if (investor) {
        return `${investor.name} #${investor.id}`
      }
    }
    return `#${entry.id}`
  }
</script>

<section class="flex flex-wrap">
  <form {id} class="w-full">
    {#each entries.filter(entriesFilter) as entry, index}
      <div class="{model}-entry">
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
              {index + 1}. {modelName}
              <small class="text-sm text-gray-500">
                {getDisplayLabel(entry)}
              </small>
            </h3>
          </div>
          <button
            class="flex-initial p-2"
            on:click|stopPropagation={() => removeEntry(entry)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if activeEntry === index}
          <div transition:slide={{ duration: 200 }}>
            {#each fields as fieldname}
              <EditField {fieldname} bind:value={entry[fieldname]} {model} />
            {/each}
          </div>
        {/if}
      </div>
    {/each}
    <div class="mt-6">
      <button
        type="button"
        class="btn btn-primary flex items-center"
        on:click={addEntry}
      >
        <PlusIcon class="-ml-2 mr-2 h-6 w-5" />
        {$_("Add")}
        {modelName}
      </button>
    </div>
  </form>
</section>
