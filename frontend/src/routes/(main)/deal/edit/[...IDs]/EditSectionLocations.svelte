<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { Location2 } from "$lib/types/newtypes"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import TextField from "$components/Fields/Edit2/TextField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let locations: Location2[]
  let activeEntryIdx = -1

  function addEntry() {
    const currentIDs = locations.map(entry => entry.nid)
    locations = [...locations, new Location2(newNanoid(currentIDs))]
    activeEntryIdx = locations.length - 1
  }

  function toggleActiveEntry(index: number): void {
    activeEntryIdx = activeEntryIdx === index ? -1 : index
  }

  function removeEntry(c: Location2) {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Location")} #${c.nid}}?`)
      if (!areYouSure) return
    }
    locations = locations.filter(x => x.nid !== c.nid)
  }
</script>

{JSON.stringify(locations)}
<section class="flex flex-wrap">
  <form class="w-full" id="locations">
    {#each locations as location, index}
      <div class="location-entry">
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
              {index + 1}. {$_("Location")}
              <small class="text-sm text-gray-500">
                #{location.nid}
                <!--{getDisplayLabel(entry)}-->
              </small>
            </h3>
          </div>
          <button
            class="flex-initial p-2"
            on:click|stopPropagation={() => removeEntry(location)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if activeEntryIdx === index}
          <div transition:slide={{ duration: 200 }}>
            <TextField
              fieldname="location.name"
              bind:value={location.name}
              label={$_("Location")}
            />
            <TextField
              fieldname="location.comment"
              bind:value={location.comment}
              label={$_("Comment")}
            />
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
        {$_("Location")}
      </button>
    </div>
  </form>
</section>
