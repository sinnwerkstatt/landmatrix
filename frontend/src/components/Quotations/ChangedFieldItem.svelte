<script lang="ts">
  import type { Snippet } from "svelte"

  import type { DataSource, QuotationItem } from "$lib/types/data"

  import CheckIcon from "$components/icons/CheckIcon.svelte"
  import XIcon from "$components/icons/XIcon.svelte"

  interface Props {
    children: Snippet
    onClick: () => void
    selectable?: boolean
    oldQuotes?: QuotationItem[]
    newQuotes?: QuotationItem[]
    oldDataSources?: DataSource[]
    newDataSources?: DataSource[]
  }
  let {
    onClick,
    selectable = true,
    children,
    oldQuotes = [],
    newQuotes = [],
    oldDataSources = [],
    newDataSources = [],
  }: Props = $props()

  let isSelected = $state(false)

  const dsEqual = $derived(
    oldQuotes.length === newQuotes.length &&
      oldQuotes.every(q => newQuotes.map(q => q.nid).includes(q.nid)),
  )
  const isValidAssignment = $derived(newQuotes.length > 0 && !dsEqual)
</script>

<button
  type="button"
  class="flex gap-2 border-2 p-2 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:dark:bg-gray-800"
  class:selected={isSelected}
  onclick={() => {
    isSelected = !isSelected
    onClick()
  }}
  disabled={!selectable}
>
  <span class="flex basis-3/4 flex-col text-left">
    {@render children()}
  </span>

  <span class="flex basis-1/4 flex-col text-right">
    {#if selectable}
      {#if isValidAssignment}
        <ins><CheckIcon /></ins>
      {:else}
        <del><XIcon /></del>
      {/if}
    {:else}
      <span>DISABLED</span>
    {/if}

    <span class="flex items-center justify-end gap-2">
      <span>
        {oldQuotes.length > 0
          ? oldQuotes
              .map(q => oldDataSources.findIndex(ds => ds.nid === q.nid) + 1)
              .join(", ")
          : ""}
      </span>
      <span>&RightArrow;</span>
      <span>
        {newQuotes.length > 0
          ? newQuotes
              .map(q => newDataSources.findIndex(ds => ds.nid === q.nid) + 1)
              .join(", ")
          : ""}
      </span>
    </span>
  </span>
</button>

<style lang="postcss">
  .selected {
    @apply border-yellow bg-yellow/20;
  }
</style>
