<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { DataSource } from "$lib/types/newtypes"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import TextField from "$components/Fields/Edit2/TextField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let datasources: DataSource[]
  let activeEntryIdx = -1

  function addEntry() {
    const currentIDs = datasources.map(entry => entry.nid)
    datasources = [...datasources, new DataSource(newNanoid(currentIDs))]
    activeEntryIdx = datasources.length - 1
  }

  function toggleActiveEntry(index: number): void {
    activeEntryIdx = activeEntryIdx === index ? -1 : index
  }

  function removeEntry(c: DataSource) {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Data source")} #${c.nid}}?`)
      if (!areYouSure) return
    }
    datasources = datasources.filter(x => x.nid !== c.nid)
  }
</script>

{JSON.stringify(datasources)}
<section class="flex flex-wrap">
  <form class="w-full" id="datasources">
    {#each datasources as datasource, index}
      <div class="datasource-entry">
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
              {index + 1}. {$_("Data source")}
              <small class="text-sm text-gray-500">
                #{datasource.nid}
                <!--{getDisplayLabel(entry)}-->
              </small>
            </h3>
          </div>
          <button
            class="flex-initial p-2"
            on:click|stopPropagation={() => removeEntry(datasource)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if activeEntryIdx === index}
          <div transition:slide={{ duration: 200 }}>
            <TextField
              fieldname="datasource.url"
              bind:value={datasource.url}
              label={$_("URL")}
            />
            <TextField
              fieldname="datasource.comment"
              bind:value={datasource.comment}
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
        {$_("Data source")}
      </button>
    </div>
  </form>
</section>
