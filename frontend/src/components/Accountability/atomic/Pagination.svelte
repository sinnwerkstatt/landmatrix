<script lang="ts">
  import IconChevron from "../icons/IconChevron.svelte"

  let paginationBox: HTMLElement|undefined = $state()
  let ellipsis = $state("none")
  let currentPage = $state(1)

  export const containerHeight = "400"

  interface Props {
    box: HTMLElement
    dataset: any // Send the dataset to pagination
    pageContent?: any // Pagination stores here what must be displayed
    detached?: boolean
    rowHeight?: string
    rowsDelta?: number // Positive = add rows, Negative = remove rows
    rowsByPage: any // Number of rows by page, if needed outside (like in Table.svelte)
    justify?: "center" | "left" | "right"
    pagination?: any
    children?: import("svelte").Snippet
  }

  let {
    box = $bindable(),
    dataset = $bindable(),
    pageContent = $bindable([]),
    detached = false,
    rowHeight = "56",
    rowsDelta = detached ? -2 : 0,
    rowsByPage = $bindable(),
    justify = "center",
    pagination = $bindable({}),
    children,
  }: Props = $props()

  function resetPageOnDataChange(dataset) {
    console.log(dataset)
    currentPage = 1
  }

  $effect(() => {
    resetPageOnDataChange(dataset)
  })

  let boxHeight = $derived(box?.getBoundingClientRect().height)
  $effect(() => {
    rowsByPage =
      (boxHeight >= rowHeight ? Math.floor(boxHeight / rowHeight) : 4) + rowsDelta
  })
  let totalPages = $derived(Math.ceil(dataset.length / rowsByPage))

  let end = $derived(currentPage * rowsByPage)
  let start = $derived(end - rowsByPage)

  $effect(() => {
    pageContent = dataset.slice(start, end)
  })

  function updatePagination(start, end, dataset) {
    const first = start + 1
    const last = end > dataset.length ? dataset.length : end
    const total = dataset.length
    return { first, last, total }
  }

  $effect(() => {
    pagination = updatePagination(start, end, dataset)
  })

  function createArray(i) {
    let array = []
    for (let j = 0; j < i; j++) {
      array.push(j)
    }
    return array
  }

  function focusOnCurrentPage(currentPage, totalPagesArray) {
    if (totalPages <= paginationButtons) {
      ellipsis = "none"
      return totalPagesArray
    }

    const midpoint = Math.floor(paginationButtons / 2)

    if (currentPage - midpoint <= 0) {
      ellipsis = "end"
      return totalPagesArray.slice(0, paginationButtons - 1)
    } else if (currentPage + midpoint >= totalPages) {
      ellipsis = "beginning"
      return totalPagesArray.slice(totalPagesArray.length - paginationButtons + 1)
    } else {
      ellipsis = "both"
      return totalPagesArray.slice(currentPage - midpoint, currentPage + midpoint - 1)
    }
  }

  let totalPagesArray = $derived(createArray(totalPages))
  let paginationButtons = $derived(
    Math.floor(paginationBox?.getBoundingClientRect().width / 24) - 2,
  )
  let focusedPagesButtons = $derived(focusOnCurrentPage(currentPage, totalPagesArray))
</script>

<div class="flex h-full flex-col overflow-hidden" class:detached>
  {#if !detached}
    <div class="h-full overflow-y-scroll" bind:this={box}>
      {@render children?.()}
    </div>
  {/if}

  <div class="pagination flex justify-{justify}" bind:this={paginationBox}>
    <button
      class="rounded-s-lg"
      disabled={currentPage === 1}
      onclick={() => {
        currentPage -= 1
      }}
    >
      <span class="-rotate-90"><IconChevron /></span>
    </button>
    {#if ellipsis === "beginning" || ellipsis === "both"}
      <button disabled>…</button>
    {/if}
    {#each focusedPagesButtons as p}
      {@const page = p + 1}
      <button
        class:selected={currentPage === page}
        onclick={() => {
          currentPage = page
        }}
      >
        {page}
      </button>
    {/each}
    {#if ellipsis === "end" || ellipsis === "both"}
      <button disabled>…</button>
    {/if}
    <button
      class="rounded-e-lg"
      disabled={currentPage === totalPages}
      onclick={() => {
        currentPage += 1
      }}
    >
      <span class="rotate-90"><IconChevron /></span>
    </button>
  </div>
</div>

<style>
  .detached {
    @apply h-fit;
  }
  .pagination button {
    @apply h-8 w-8;
    @apply grid place-content-center;
    @apply bg-white text-a-gray-500;
    @apply border border-a-gray-200;
  }
  .pagination button:hover,
  .pagination button:disabled {
    @apply bg-a-gray-50;
  }
  .pagination button.selected {
    @apply text-a-gray-900;
  }
</style>
