<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { Contract } from "$lib/types/newtypes"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import EditField from "$components/Fields/EditField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let contracts: Contract[]
  let activeEntryIdx = -1

  const addEntry = () => {
    const currentIDs = contracts.map(entry => entry.nid)
    contracts = [...contracts, new Contract(newNanoid(currentIDs))]
    activeEntryIdx = contracts.length - 1
  }

  const removeEntry = (c: Contract) => {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Contract")} #${c.nid}}?`)
      if (!areYouSure) return
    }
    contracts = contracts.filter(x => x.nid !== c.nid)
  }

  const toggleActiveEntry = (index: number) =>
    (activeEntryIdx = activeEntryIdx === index ? -1 : index)
</script>

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
            <EditField
              fieldname="contract.number"
              bind:value={contract.number}
              showLabel
            />
            <EditField fieldname="contract.date" bind:value={contract.date} showLabel />
            <EditField
              fieldname="contract.expiration_date"
              bind:value={contract.expiration_date}
              showLabel
            />
            <EditField
              fieldname="contract.agreement_duration"
              bind:value={contract.agreement_duration}
              showLabel
            />
            <EditField
              fieldname="contract.comment"
              bind:value={contract.comment}
              showLabel
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
