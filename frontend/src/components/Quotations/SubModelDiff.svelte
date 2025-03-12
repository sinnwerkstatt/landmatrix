<script lang="ts">
  import { detailedDiff } from "deep-object-diff"
  import { _ } from "svelte-i18n"

  import { getTypedKeys } from "$lib/helpers"
  import type { DataSource, SubmodelQuotations } from "$lib/types/data"

  import ChangedFieldItem from "$components/Quotations/ChangedFieldItem.svelte"
  import { toggleSelected } from "$components/Quotations/selectedPaths.svelte"
  import { mergeKeys } from "$components/Quotations/utils"

  interface SubModelEntry {
    nid: string
    id: number
  }

  interface Props {
    key: string
    label: string
    oldEntries?: SubModelEntry[]
    newEntries?: SubModelEntry[]
    oldQuotations?: SubmodelQuotations
    newQuotations?: SubmodelQuotations
    oldDataSources?: DataSource[]
    newDataSources?: DataSource[]
  }

  type DiffType = keyof ReturnType<typeof detailedDiff>

  const TYPE_LABELS = $derived({
    added: $_("added"),
    deleted: $_("deleted"),
    updated: $_("updated"),
  })

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

  const createNidLookup = (entries: SubModelEntry[]) =>
    entries.reduce((acc, current) => ({ ...acc, [current.nid]: current }), {})

  const entriesDiff = $derived(
    detailedDiff(createNidLookup(oldEntries), createNidLookup(newEntries)),
  )
  const quotationsDiff = $derived(detailedDiff(oldQuotations, newQuotations))

  const createLabel = (type: DiffType, nid: string) => {
    const originalIdx = oldEntries.findIndex(obj => obj.nid === nid)
    const updatedIdx = newEntries.findIndex(obj => obj.nid === nid)

    const lookup: { [key in DiffType]: number } = {
      added: updatedIdx,
      updated: updatedIdx,
      deleted: originalIdx,
    }
    return `${lookup[type] + 1}. ${label}`
  }
</script>

<div class="flex flex-col gap-2">
  {#each getTypedKeys(TYPE_LABELS) as type}
    <!--TODO: Fix can update value but add quotation for same nid-->
    {@const hasValueChange = Object.keys(entriesDiff[type]).length > 0}
    {@const mergedKeys = mergeKeys(entriesDiff[type], quotationsDiff[type])}

    {#each mergedKeys as nid}
      {@const label = createLabel(type, nid)}

      <ChangedFieldItem
        selectable={type !== "deleted" && key !== "datasources"}
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
          {#if hasValueChange}
            {TYPE_LABELS[type]}
          {:else}
            <span class="italic">{$_("No value change")}</span>
          {/if}
        </span>
      </ChangedFieldItem>
    {/each}
  {/each}
</div>
