<script lang="ts">
  import IconChevron from "../icons/IconChevron.svelte"

  let paginationBox: HTMLElement
  let ellipsis = "none"
  let currentPage = 1

  export let box: HTMLElement // Needs to be binded to the data container (ex: table body) when detached
  export let dataset // Send the dataset to pagination
  export let pageContent = [] // Pagination stores here what must be displayed
  export let detached = false
  export const containerHeight = "400"
  export let rowHeight = "56"
  export let rowsDelta: number = detached ? -2 : 0 // Positive = add rows, Negative = remove rows
  export let rowsByPage // Number of rows by page, if needed outside (like in Table.svelte)
  export let justify: "center" | "left" | "right" = "center"

  export let pagination = {}

  function resetPageOnDataChange(dataset) {
    console.log(dataset)
    currentPage = 1
  }

  $: resetPageOnDataChange(dataset)

  $: boxHeight = box?.getBoundingClientRect().height
  $: rowsByPage =
    (boxHeight >= rowHeight ? Math.floor(boxHeight / rowHeight) : 4) + rowsDelta
  $: totalPages = Math.ceil(dataset.length / rowsByPage)

  $: end = currentPage * rowsByPage
  $: start = end - rowsByPage

  $: pageContent = dataset.slice(start, end)

  function updatePagination(start, end, dataset) {
    const first = start + 1
    const last = end > dataset.length ? dataset.length : end
    const total = dataset.length
    return { first, last, total }
  }

  $: pagination = updatePagination(start, end, dataset)

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

  $: totalPagesArray = createArray(totalPages)
  $: paginationButtons =
    Math.floor(paginationBox?.getBoundingClientRect().width / 24) - 2
  $: focusedPagesButtons = focusOnCurrentPage(currentPage, totalPagesArray)
</script>

<div class="flex h-full flex-col overflow-hidden" class:detached>
  {#if !detached}
    <div class="h-full overflow-y-scroll" bind:this={box}>
      <slot />
    </div>
  {/if}

  <div class="pagination flex justify-{justify}" bind:this={paginationBox}>
    <button
      class="rounded-s-lg"
      disabled={currentPage === 1}
      on:click={() => {
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
        on:click={() => {
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
      on:click={() => {
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
