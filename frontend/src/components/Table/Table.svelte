<script module lang="ts">
  export interface Column {
    key: string
    label: string
    colSpan: number
    submodel?: string
  }
</script>

<script lang="ts" generics="T extends object">
  import { onMount, type Snippet } from "svelte"
  import VirtualList from "svelte-tiny-virtual-list"
  import { twMerge } from "tailwind-merge"

  import { sortFn } from "$lib/utils"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  interface Props {
    /* eslint-disable no-undef */
    items?: T[]
    /* eslint-enable no-undef */
    columns: Column[]
    sortBy?: string | null
    rowHeightInPx?: number
    headerHeightInPx?: number
    colWidthInPx?: number
    rowClasses?: string
    field?: Snippet<{ fieldName: string; obj: T }[]>
  }

  let {
    items = [],
    columns,
    sortBy = $bindable(),
    rowHeightInPx = 90,
    headerHeightInPx = 90,
    colWidthInPx = 75,
    rowClasses = "",
    field,
  }: Props = $props()

  let labels: string[] = $derived(columns.map(c => c.label))
  let spans: number[] = $derived(columns.map(c => c.colSpan))

  let sortCol = $derived(
    columns.find(
      c => c.key === (sortBy?.startsWith("-") ? sortBy.substring(1) : sortBy),
    ),
  )
  let sortedItems = $derived(
    sortCol
      ? [...items].sort(
          sortFn(
            (sortBy?.startsWith("-") ? "-" : "") +
              (sortCol.submodel ? `${sortCol.submodel}.${sortCol.key}` : sortCol.key),
          ),
        )
      : items,
  )
  let nItems = $derived(sortedItems?.length ?? 0)

  let nCols = $derived(spans.reduce((sum, value) => sum + value))

  const onTableHeadClick = (key: string) => {
    sortBy = sortBy === key ? `-${key}` : key
  }

  let virtualList: VirtualList | undefined = $state()
  let width: number | undefined = $state()
  let height: number | undefined = $state()

  onMount(() => virtualList?.recomputeSizes(0))
</script>

<div class="h-full w-full border border-gray-700">
  <div
    bind:clientWidth={width}
    bind:clientHeight={height}
    class={twMerge(
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
          ? 'items-center bg-gray-700 font-medium text-white dark:bg-gray-800 dark:text-white'
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
              onclick={() => onTableHeadClick(col.key)}
              title={labels[colIndex]}
            >
              {labels[colIndex]}

              <span class="relative pl-1">
                <ChevronDownIcon
                  class={twMerge(
                    "absolute top-0 inline h-4 w-4 rotate-180 rounded",
                    sortBy === `-${col.key}` ? "text-orange" : "text-gray-400",
                  )}
                />
                <ChevronDownIcon
                  class={twMerge(
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
              {#if field}
                {@render field({
                  fieldName: col.key,
                  obj: sortedItems[index - 1],
                })}
              {:else if col.submodel}
                {sortedItems[index - 1][col.submodel][col.key]}
              {:else}
                {sortedItems[index - 1][col.key]}
              {/if}
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
