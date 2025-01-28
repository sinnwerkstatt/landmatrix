<script lang="ts" module>
  export interface SubModelEntry {
    nid: string
    id: number
  }
</script>

<script lang="ts">
  import { detailedDiff } from "deep-object-diff"
  import { _ } from "svelte-i18n"

  import { getTypedKeys } from "$lib/helpers"

  import SubModelEntryDiff from "$components/DSQuotations/SubModelEntryDiff.svelte"
  import type { SubModel } from "$components/ReviewChangesModal.svelte"

  interface Props {
    subModel: SubModel
    original: SubModelEntry[]
    updated: SubModelEntry[]
  }

  let { subModel, original = [], updated = [] }: Props = $props()

  const createNidLookup = (entries: SubModelEntry[]) =>
    entries.reduce((acc, current) => ({ ...acc, [current.nid]: current }), {})

  const diff = $derived(
    detailedDiff(createNidLookup(original), createNidLookup(updated)),
  )

  const counts = $derived({
    added: Object.keys(diff["added"]).length,
    updated: Object.keys(diff["updated"]).length,
    deleted: Object.keys(diff["deleted"]).length,
  })
</script>

<div>
  <p>
    <span class="after:content-[':']">
      {subModel.label}
    </span>

    {#if counts["added"]}
      <span class="text-green">
        {counts["added"]}
        {$_("Added")}
      </span>
    {/if}

    {#if counts["updated"]}
      <span class="text-yellow">
        {counts["updated"]}
        {$_("Updated")}
      </span>
    {/if}

    {#if counts["deleted"]}
      <span class="text-red">
        {counts["deleted"]}
        {$_("Deleted")}
      </span>
    {/if}
  </p>

  <div class="flex flex-col gap-2">
    {#each getTypedKeys(diff) as type}
      {#each getTypedKeys(diff[type]) as nid}
        {@const originalIdx = original.findIndex(obj => obj.nid === nid)}
        {@const updatedIdx = updated.findIndex(obj => obj.nid === nid)}

        <SubModelEntryDiff
          {type}
          {nid}
          original={original[originalIdx]}
          updated={updated[updatedIdx]}
          diff={diff[type][nid]}
        />
      {/each}
    {/each}
  </div>
</div>
