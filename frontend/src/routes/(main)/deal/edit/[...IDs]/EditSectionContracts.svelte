<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { Contract } from "$lib/types/newtypes"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import TextField from "$components/Fields/Edit2/TextField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let contracts: Contract[]
  let activeEntryIdx = -1

  function addEntry() {
    const currentIDs = contracts.map(entry => entry.nid)
    contracts = [...contracts, new Contract(newNanoid(currentIDs))]
    activeEntryIdx = contracts.length - 1
  }

  function toggleActiveEntry(index: number): void {
    activeEntryIdx = activeEntryIdx === index ? -1 : index
  }

  function removeEntry(c: Contract) {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Contract")} #${c.nid}}?`)
      if (!areYouSure) return
    }
    contracts = contracts.filter(x => x.nid !== c.nid)
  }
</script>

{JSON.stringify(contracts)}
<section class="flex flex-wrap">
  <form class="w-full" id="contracts">
    {#each contracts as contract, index}
      <div class="contract-entry">
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
              {index + 1}. {$_("Contract")}
              <small class="text-sm text-gray-500">
                #{contract.nid}
                <!--{getDisplayLabel(entry)}-->
              </small>
            </h3>
          </div>
          <button
            class="flex-initial p-2"
            on:click|stopPropagation={() => removeEntry(contract)}
          >
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </button>
        </div>
        {#if activeEntryIdx === index}
          <div transition:slide={{ duration: 200 }}>
            <TextField
              fieldname="contract.number"
              bind:value={contract.number}
              label={$_("Contract number")}
            />
            <TextField
              fieldname="contract.comment"
              bind:value={contract.comment}
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
        {$_("Contract")}
      </button>
    </div>
  </form>
</section>
