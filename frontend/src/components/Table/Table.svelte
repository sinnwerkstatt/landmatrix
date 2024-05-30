<script context="module" lang="ts">
  export interface Column {
    key: string
    label: string
    colSpan: number
    submodel?: string
  }
</script>

<script lang="ts">
  import cn from "classnames"
  import { onMount } from "svelte"
  import VirtualList from "svelte-tiny-virtual-list"

  import { sortFn } from "$lib/utils"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  export let columns: Column[]
  export let items: unknown[] = []
  export let sortBy: string | null = null

  export let rowHeightInPx = 90
  export let headerHeightInPx = 90
  export let colWidthInPx = 75

  export let rowClasses = ""

  let labels: string[] = []
  let spans: number[] = []

  $: labels = columns.map(c => c.label)
  $: spans = columns.map(c => c.colSpan)

  $: sortCol = columns.find(
    c => c.key === (sortBy?.startsWith("-") ? sortBy.substring(1) : sortBy),
  )
  $: sortedItems = sortCol
    ? [...items].sort(
        sortFn(
          (sortBy?.startsWith("-") ? "-" : "") +
            (sortCol.submodel ? `${sortCol.submodel}.${sortCol.key}` : sortCol.key),
        ),
      )
    : items
  $: nItems = sortedItems?.length ?? 0

  $: nCols = spans.reduce((sum, value) => sum + value)

  const onTableHeadClick = (key: string) => {
    sortBy = sortBy === key ? `-${key}` : key
  }

  let virtualList: VirtualList
  let width
  let height

  onMount(() => virtualList.recomputeSizes(0))
</script>

<div class="h-full w-full border border-gray-700">
  <div
    bind:clientWidth={width}
    bind:clientHeight={height}
    class={cn(
      "h-full w-full overflow-x-auto",
      nItems % 2 ? "bg-white dark:bg-gray-600" : "bg-gray-100 dark:bg-gray-700",
    )}
  >
    <!-- height -2 as safety margin-->
    <VirtualList
      bind:this={virtualList}
      width="{width > colWidthInPx * nCols ? width : colWidthInPx * nCols}px"
      height={height - 2}
      itemCount={nItems + 1}
      itemSize={index => (index === 0 ? headerHeightInPx : rowHeightInPx)}
      stickyIndices={[0]}
    >
      <div
        slot="item"
        class="row {index === 0
          ? 'items-center bg-gray-700 font-medium text-white'
          : 'odd:bg-white even:bg-gray-100 hover:bg-gray-200 dark:odd:bg-gray-600 dark:even:bg-gray-700 dark:hover:bg-gray-500'} {rowClasses}"
        let:index
        let:style
        style="--grid-columns: {nCols}; --col-width: {colWidthInPx}px; {style}"
      >
        {#if index === 0}
          {#each columns as col, colIndex}
            <button
              class="m-0 cursor-pointer p-1 text-left"
              style="grid-column: span {spans[colIndex]} / span {spans[colIndex]}"
              on:click={() => onTableHeadClick(col.key)}
            >
              {labels[colIndex]}

              <span class="relative pl-1">
                <ChevronDownIcon
                  class={cn(
                    "absolute top-0 inline h-4 w-4 rotate-180 rounded",
                    sortBy === `-${col.key}` ? "text-orange" : "text-gray-400",
                  )}
                />
                <ChevronDownIcon
                  class={cn(
                    "absolute top-2 inline h-4 w-4 rounded",
                    sortBy === col.key ? "text-orange" : "text-gray-400",
                  )}
                />
              </span>
            </button>
          {/each}
        {:else}
          {#each columns as col, colIndex}
            <!-- Testing slots not possible atm -->
            <!-- https://github.com/testing-library/svelte-testing-library/issues/48#issuecomment-522029988-->
            <div
              data-testid="{index - 1}-{colIndex}"
              class="overflow-hidden p-1 hover:overflow-y-auto"
              style="grid-column: span {spans[colIndex]} / span {spans[colIndex]}"
            >
              <slot name="field" fieldName={col.key} obj={sortedItems[index - 1]}>
                {#if col.submodel}
                  {sortedItems[index - 1][col.submodel][col.key]}
                {:else}
                  {sortedItems[index - 1][col.key]}
                {/if}
              </slot>
            </div>
          {/each}
        {/if}
      </div>
    </VirtualList>
  </div>
</div>

<style lang="css">
  .row {
    display: grid;
    grid-template-columns: repeat(var(--grid-columns), var(--col-width));
  }

  :global(.virtual-list-inner) {
    overflow-x: clip !important;
  }
</style>
