<script lang="ts">
  import { diff } from "deep-object-diff"
  import { _ } from "svelte-i18n"

  import type { DataSource, SubmodelQuotations } from "$lib/types/data"

  import ChangedFieldItem from "$components/Quotations/ChangedFieldItem.svelte"
  import type { SubmodelKey } from "$components/Quotations/ReviewChangesModal.svelte"
  import { toggleSelected } from "$components/Quotations/selectedPaths.svelte"
  import SubmodelPopup from "$components/Quotations/SubmodelPopup.svelte"
  import { mergeKeys } from "$components/Quotations/utils"

  interface SubModelEntry {
    nid: string
    id: number
  }

  interface Props {
    key: SubmodelKey
    label: string
    oldEntries?: SubModelEntry[]
    newEntries?: SubModelEntry[]
    oldQuotations?: SubmodelQuotations
    newQuotations?: SubmodelQuotations
    oldDataSources?: DataSource[]
    newDataSources?: DataSource[]
  }

  let {
    key,
    label,
    oldEntries = [],
    newEntries = [],
    oldQuotations = {},
    newQuotations = {},
    oldDataSources = [],
    newDataSources = [],
  }: Props = $props()

  const createNidLookup = (
    entries: SubModelEntry[],
  ): { [key: string]: SubModelEntry } =>
    entries.reduce((acc, current) => ({ ...acc, [current.nid]: current }), {})

  const oldEntriesLookup = $derived(createNidLookup(oldEntries))
  const newEntriesLookup = $derived(createNidLookup(newEntries))
  const entriesDiff = $derived(
    diff(oldEntriesLookup, newEntriesLookup) as { [key: string]: SubModelEntry },
  )

  const quotationsDiff = $derived(diff(oldQuotations, newQuotations))

  const mergedKeys = $derived(mergeKeys(entriesDiff, quotationsDiff))
</script>

<div class="flex flex-col gap-2">
  {#each mergedKeys as nid}
    {@const isInOld = !!(nid in oldEntriesLookup)}
    {@const isInNew = !!(nid in newEntriesLookup)}
    {@const isAdded = !isInOld && isInNew}
    {@const isDeleted = isInOld && !isInNew}
    {@const hasValueChange = !!(nid in entriesDiff)}

    <ChangedFieldItem
      selectable={!isDeleted && key !== "datasources"}
      onClick={() => toggleSelected([key, nid])}
      oldQuotes={oldQuotations[nid]}
      newQuotes={newQuotations[nid]}
      {oldDataSources}
      {newDataSources}
    >
      <span class="flex flex-col text-left">
        <span>
          {label}
          <small class="font-oswald text-sm text-gray-500">
            #{nid}
          </small>
        </span>
        <span class="italic">
          {#if isDeleted}
            {$_("Deleted")}
            <SubmodelPopup {key} entry={oldEntriesLookup[nid]} {label} />
          {:else if isAdded}
            {$_("Added")}
            <SubmodelPopup {key} entry={newEntriesLookup[nid]} {label} />
          {:else if hasValueChange}
            {$_("Updated")}
            <SubmodelPopup {key} entry={oldEntriesLookup[nid]} {label} />
            <span>&RightArrow;</span>
            <SubmodelPopup {key} entry={newEntriesLookup[nid]} {label} />
          {:else}
            {$_("No value change")}
          {/if}
        </span>
      </span>
    </ChangedFieldItem>
  {/each}
</div>
