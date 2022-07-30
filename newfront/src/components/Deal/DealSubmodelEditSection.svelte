<script lang="ts">
  import { _ } from "svelte-i18n";
  import { slide } from "svelte/transition";
  import { newNanoid } from "$lib/helpers";
  import { subsections } from "$lib/sections";
  import type { Contract, DataSource } from "$lib/types/deal";
  import { isEmptySubmodel } from "$lib/utils/data_processing";
  import EditField from "$components/Fields/EditField.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import TrashIcon from "$components/icons/TrashIcon.svelte";

  export let model: string;
  export let modelName: string;
  export let entries: Array<Contract | DataSource> = [];
  export let id: string;

  // TODO: build something to filter out empty entries
  // $: _entries = JSON.parse(JSON.stringify(entries));

  $: fields = subsections[model];

  let activeEntry: number;
  $: activeEntry = 0; //entries.length - 1;

  function addEntry() {
    const currentIDs = entries.map((x) => x.id.toString());
    const newEntry = { id: newNanoid(currentIDs) } as Contract | DataSource;
    entries = [...entries, newEntry];
  }

  function removeEntry(entry: Contract | DataSource) {
    if (isEmptySubmodel(entry)) {
      entries = entries.filter((x) => x.id !== entry.id);
      return;
    }
    const areYouSure = confirm(`${$_("Remove")} ${$_(modelName)} ${entry.id}?`);
    if (areYouSure === true) entries = entries.filter((x) => x.id !== entry.id);
  }
</script>

<section class="flex flex-wrap">
  <form {id} class="w-full">
    {#each entries as entry, index}
      <div class="{model}-entry">
        <h3 on:click={() => (activeEntry = activeEntry === index ? -1 : index)}>
          {index + 1}. {$_(modelName)}
          <small class="text-sm text-gray-500">#{entry.id}</small>
          <TrashIcon
            class="w-6 h-6 text-red-600 float-right cursor-pointer"
            on:click={() => removeEntry(entry)}
          />
        </h3>
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
        <PlusIcon class="w-5 h-6 mr-2 -ml-2" />
        {$_("Add")}
        {$_(modelName)}
      </button>
    </div>
  </form>
</section>
