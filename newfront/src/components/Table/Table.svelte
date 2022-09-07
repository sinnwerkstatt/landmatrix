<script lang="ts">
  import classNames from "classnames"
  import { onMount } from "svelte"
  import VirtualList from "svelte-tiny-virtual-list"

  import { sortFn } from "$lib/utils"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  export let columns: string[]
  export let labels: string[] | null = null
  export let spans: number[] | null = null
  export let items: Array<{ [key: string]: unknown }> = []
  export let sortBy: string | null = null

  export let rowHeightInPx = 90
  export let headerHeightInPx = 40
  export let colWidthInPx = 70

  export let rowClasses = ""

  $: sortedItems = sortBy ? [...items].sort(sortFn(sortBy)) : items

  $: labels = labels ?? columns
  $: spans = spans ?? columns.map(col => 1)
  $: nCols = spans.reduce((sum, value) => sum + value)

  const onTableHeadClick = col => {
    sortBy = sortBy === col ? `-${col}` : col
  }

  let virtualList: VirtualList
  let width
  let height

  onMount(() => virtualList.recomputeSizes(0))
</script>

<div
  bind:clientWidth={width}
  bind:clientHeight={height}
  class="h-full w-full overflow-x-auto border border-gray-700"
>
  <VirtualList
    bind:this={virtualList}
    width="{width > colWidthInPx * nCols ? width : colWidthInPx * nCols}px"
    {height}
    itemCount={sortedItems.length + 1}
    itemSize={index => (index === 0 ? headerHeightInPx : rowHeightInPx)}
    stickyIndices={[0]}
  >
    <div
      slot="item"
      class="row {index === 0
        ? 'whitespace-nowrap bg-gray-700 pr-4 font-medium text-white'
        : 'odd:bg-white even:bg-gray-100 hover:bg-gray-200'} {rowClasses}"
      let:index
      let:style
      style="--grid-columns: {nCols}; --col-width: {colWidthInPx}px; {style}"
    >
      {#if index === 0}
        {#each columns as col, colIndex}
          <div
            class="cursor-pointer p-1"
            style="grid-column: span {spans[colIndex]} / span {spans[colIndex]}"
            on:click={() => onTableHeadClick(col)}
          >
            {labels[colIndex]}
            {#if sortBy === col || sortBy === `-${col}`}
              <ChevronDownIcon
                class={classNames(
                  "transition-duration-300 inline h-4 w-4 rounded text-orange transition-transform",
                  sortBy === `-${col}` ? "rotate-180" : "",
                )}
              />
            {/if}
          </div>
        {/each}
      {:else}
        {#each columns as fieldName, colIndex}
          <!-- Testing slots not possible atm -->
          <!-- https://github.com/testing-library/svelte-testing-library/issues/48#issuecomment-522029988-->
          <div
            data-testid="{index - 1}-{colIndex}"
            class="overflow-hidden p-1 hover:overflow-y-auto"
            style="grid-column: span {spans[colIndex]} / span {spans[colIndex]}"
          >
            <slot name="field" {fieldName} obj={sortedItems[index - 1]}>
              {sortedItems[index - 1][fieldName]}
            </slot>
          </div>
        {/each}
      {/if}
    </div>
  </VirtualList>
</div>

<style>
  .row {
    display: grid;
    grid-template-columns: repeat(var(--grid-columns), var(--col-width));
  }

  :global(.virtual-list-inner) {
    overflow-x: clip !important;
  }
</style>
