<script lang="ts">
  import classNames from "classnames"
  import VirtualList from "svelte-tiny-virtual-list"

  import { sortFn } from "$lib/utils"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  export let columns: string[]
  export let labels: string[] | null = null
  export let spans: number[] | null = null
  export let items: Array<{ [key: string]: unknown }> = []
  export let sortBy: string | null = null
  export let rowHeightInPx = 80
  export let colWidthInPx = 80

  export let rowClasses = ""

  $: sortedItems = sortBy ? [...items].sort(sortFn(sortBy)) : items

  $: labels = labels ?? columns
  $: spans = spans ?? columns.map(col => 1)
  $: nCols = spans.reduce((sum, value) => sum + value)

  const onTableHeadClick = col => {
    sortBy = sortBy === col ? `-${col}` : col
  }

  let virtualList: VirtualList
</script>

<div class="overflow-x-auto overflow-y-hidden">
  <div class="table">
    <div
      class="row whitespace-nowrap bg-gray-700 pr-4 font-medium text-white"
      style="--grid-columns: {nCols}; --col-width: {colWidthInPx}px;"
    >
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
    </div>
    <VirtualList
      bind:this={virtualList}
      width={"100%"}
      height={650}
      itemCount={sortedItems.length}
      itemSize={rowHeightInPx}
    >
      <div
        slot="item"
        class="row odd:bg-white even:bg-gray-50 hover:bg-gray-100 {rowClasses}"
        let:index
        let:style
        style="--grid-columns: {nCols}; --col-width: {colWidthInPx}px; {style}"
      >
        {#each columns as fieldName, colIndex}
          <!-- Testing slots not possible atm -->
          <!-- https://github.com/testing-library/svelte-testing-library/issues/48#issuecomment-522029988-->
          <div
            data-testid="{index}-{colIndex}"
            class="hover:overflow-auto"
            style="grid-column: span {spans[colIndex]} / span {spans[colIndex]}"
          >
            <slot name="field" {fieldName} obj={sortedItems[index]}>
              {sortedItems[index][fieldName]}
            </slot>
          </div>
        {/each}
      </div>
    </VirtualList>
  </div>
</div>

<style>
  .row {
    display: grid;
    grid-template-columns: repeat(var(--grid-columns), var(--col-width));
  }
</style>
