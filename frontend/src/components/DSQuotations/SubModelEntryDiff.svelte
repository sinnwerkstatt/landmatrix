<script lang="ts">
  import type { DetailedDiff } from "deep-object-diff"

  import { getTypedKeys } from "$lib/helpers"

  import type { SubModelEntry } from "$components/DSQuotations/SubModelDiff.svelte"
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  interface Props {
    type: keyof DetailedDiff
    nid: string
    original: SubModelEntry
    updated: SubModelEntry
    diff: object
  }

  let { type, nid, original, updated, diff = {} }: Props = $props()

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

<div class="p-2 {classLookup[type]}">
  <button class="flex w-full items-center gap-2" onclick={() => (open = !open)}>
    <ChevronDownIcon />
    <span class="font-mono font-bold italic">{nid}</span>
    {type}
  </button>

  {#if open}
    <div>
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
