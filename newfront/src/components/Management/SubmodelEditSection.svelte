<script lang="ts">
  import { _ } from "svelte-i18n";
  import { slide } from "svelte/transition";
  import { newNanoid } from "$lib/helpers";
  import { subsections } from "$lib/sections";
  import type { Contract, DataSource } from "$lib/types/deal";
  import type { Involvement } from "$lib/types/investor";
  import { isEmptySubmodel } from "$lib/utils/data_processing";
  import EditField from "$components/Fields/EditField.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import TrashIcon from "$components/icons/TrashIcon.svelte";

  export let model: "datasource" | "contract" | "involvement";
  export let modelName: string;
  export let entries: Array<Contract | DataSource | Involvement> = [];
  export let entriesFilter: (i: Involvement) => boolean = () => true;
  export let newEntryExtras = {};
  export let id: string;

  export let fields = subsections[model];

  let activeEntry = -1;

  function addEntry() {
    const currentIDs = entries.map((x) => x?.id?.toString());
    const newEntry = { id: newNanoid(currentIDs), ...newEntryExtras } as
      | Contract
      | DataSource
      | Involvement;
    entries = [...entries, newEntry];
    activeEntry = entries.length - 1;
  }

  function removeEntry(entry: Contract | DataSource) {
    if (!isEmptySubmodel(entry)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_(modelName)} ${entry.id}?`);
      if (!areYouSure) return;
    }

    entries = entries.filter((x) => x.id !== entry.id);
  }
</script>

<section class="flex flex-wrap">
  <form {id} class="w-full">
    {#each entries.filter(entriesFilter) as entry, index}
      <div class="{model}-entry">
        <div class="my-2 flex flex-row items-center justify-between bg-gray-200">
          <div
            class="flex-grow p-2"
            on:click={() => (activeEntry = activeEntry === index ? -1 : index)}
          >
            <h3 class="m-0">
              {index + 1}. {$_(modelName)}
              <small class="text-sm text-gray-500">
                {#if model === "involvement"}
                  {#if entry?.investor?.id}
                    {$_("Investor")} #{entry.investor.id}
                  {/if}
                {:else}
                  #{entry.id}
                {/if}
              </small>
            </h3>
          </div>
          <div class="flex-initial p-2" on:click={() => removeEntry(entry)}>
            <TrashIcon class="h-8 w-6 cursor-pointer text-red-600" />
          </div>
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
        <PlusIcon class="mr-2 -ml-2 h-6 w-5" />
        {$_("Add")}
        {$_(modelName)}
      </button>
    </div>
  </form>
</section>
