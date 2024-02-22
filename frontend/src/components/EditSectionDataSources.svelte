<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { newNanoid } from "$lib/helpers"
  import { DataSource } from "$lib/types/newtypes"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"
  import EditField from "$components/Fields/EditField.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"
  import TrashIcon from "$components/icons/TrashIcon.svelte"

  export let datasources: DataSource[]

  export let investorModel = false

  let activeEntryIdx = -1

  const addEntry = () => {
    const currentIDs = datasources.map(entry => entry.nid)
    datasources = [...datasources, new DataSource(newNanoid(currentIDs))]
    activeEntryIdx = datasources.length - 1
  }

  const removeEntry = (c: DataSource) => {
    if (!isEmptySubmodel(c)) {
      const areYouSure = confirm(`${$_("Remove")} ${$_("Data source")} #${c.nid}}?`)
      if (!areYouSure) return
    }
    datasources = datasources.filter(x => x.nid !== c.nid)
  }

  const toggleActiveEntry = (index: number) =>
    (activeEntryIdx = activeEntryIdx === index ? -1 : index)
</script>

<section class="my-6 flex flex-wrap">
  <form class="w-full" id="data_sources">
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
            <EditField
              fieldname="datasource.type"
              bind:value={datasource.type}
              showLabel
            />

            <EditField
              fieldname="datasource.url"
              bind:value={datasource.url}
              showLabel
            />

            <EditField
              fieldname="datasource.file"
              showLabel
              bind:value={datasource.file}
            >
              <label for={undefined} class="my-2 flex items-center gap-2">
                <LowLevelNullBooleanField
                  bind:value={datasource.file_not_public}
                  fieldname="datasource.file_not_public"
                />
                {$_("Keep PDF not public")}
              </label>
            </EditField>

            <EditField
              fieldname="datasource.publication_title"
              bind:value={datasource.publication_title}
              showLabel
            />
            <EditField
              fieldname="datasource.date"
              bind:value={datasource.date}
              showLabel
            />
            <EditField
              fieldname="datasource.name"
              bind:value={datasource.name}
              showLabel
            />
            <EditField
              fieldname="datasource.company"
              bind:value={datasource.company}
              showLabel
            />
            <EditField
              fieldname="datasource.email"
              bind:value={datasource.email}
              showLabel
            />
            <EditField
              fieldname="datasource.phone"
              bind:value={datasource.phone}
              showLabel
            />
            <EditField
              fieldname="datasource.includes_in_country_verified_information"
              bind:value={datasource.includes_in_country_verified_information}
              showLabel
            />
            <EditField
              fieldname="datasource.open_land_contracts_id"
              bind:value={datasource.open_land_contracts_id}
              showLabel
            />
            <EditField
              fieldname="datasource.comment"
              bind:value={datasource.comment}
              showLabel
            />
          </div>
        {/if}
      </div>
    {/each}
    <div class="mt-6">
      <button
        class="butn {investorModel
          ? 'butn-secondary'
          : 'butn-primary'} flex items-center"
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
