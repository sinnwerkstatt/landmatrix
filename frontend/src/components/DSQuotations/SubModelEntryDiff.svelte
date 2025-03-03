<script lang="ts">
  import type { DetailedDiff } from "deep-object-diff"

  import { getTypedKeys } from "$lib/helpers"

  import type { SubModelEntry } from "$components/DSQuotations/SubModelDiff.svelte"
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import type { SubModel } from "$components/ReviewChangesModal.svelte"

  interface Props {
    subModel: SubModel
    type: keyof DetailedDiff
    nid: string
    original: SubModelEntry
    updated: SubModelEntry
    diff: object
  }

  let { subModel, type, nid, original, updated, diff = {} }: Props = $props()

  let open = $state(false)

  const classLookup: { [key in keyof DetailedDiff]: string } = {
    added: "border-2 border-green",
    deleted: "border-2 border-red",
    updated: "border-2 border-yellow",
  }

  const submodelIgnoreKeys = ["id", "nid", "dealversion", "investorversion"]

  const fieldKeys = $derived(
    getTypedKeys(diff).filter(key => !submodelIgnoreKeys.includes(key)),
  )
</script>

<div class={classLookup[type]}>
  <button
    type="button"
    class="flex w-full items-center gap-2 p-2"
    onclick={() => (open = !open)}
  >
    <ChevronDownIcon />
    {subModel.label}
    {type}
    <span class="font-mono font-bold italic">{nid}</span>
  </button>

  {#if open}
    <div class="border-t-2 p-2">
      {#each fieldKeys as fieldKey}
        <div class="flex pl-5">
          <span class="basis-1/3">{fieldKey}</span>
          <span class="basis-1/3">
            {original?.[fieldKey] ?? "--"}
          </span>
          <span class="basis-1/3">
            {updated?.[fieldKey] ?? "--"}
          </span>
        </div>
      {/each}
    </div>
  {/if}
</div>
