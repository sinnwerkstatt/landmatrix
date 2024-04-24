<script lang="ts">
    import IconChevron from "../icons/IconChevron.svelte"

    let box:HTMLElement
    let paginationBox:HTMLElement
    let currentPage = 1
    let ellipsis = "none"

    export let dataset
    export let pageContent = []
    export let containerHeight = "400"
    export let rowHeight = "56"

    $: boxHeight = box?.getBoundingClientRect().height;
    $: rowsByPage = boxHeight >= rowHeight ? Math.floor(boxHeight / rowHeight) : 4;
    $: totalPages = Math.ceil(dataset.length / rowsByPage);

    $: end = currentPage * rowsByPage;
    $: start = end - rowsByPage;

    $: pageContent = dataset.slice(start, end);

    function createArray(i) {
        let array = [];
        for (let j = 0; j < i; j++) {
            array.push(j);
        }
        return array;
    }

    function focusOnCurrentPage(currentPage, totalPagesArray) {
        if (totalPages <= paginationButtons) {
            ellipsis = "none";
            return totalPagesArray;
        }

        const midpoint = Math.floor(paginationButtons / 2);

        if (currentPage - midpoint <= 0) {
            ellipsis = "end";
            return totalPagesArray.slice(0, paginationButtons - 1);
        } else if (currentPage + midpoint >= totalPages) {
            ellipsis = "beginning";
            return totalPagesArray.slice(totalPagesArray.length - paginationButtons + 1);
        } else {
            ellipsis = "both";
            return totalPagesArray.slice(currentPage - midpoint, currentPage + midpoint - 1);
        }
    }

    $: totalPagesArray = createArray(totalPages);
    $: paginationButtons = Math.floor(paginationBox?.getBoundingClientRect().width / 24) - 2;
    $: focusedPagesButtons = focusOnCurrentPage(currentPage, totalPagesArray);

</script>

<div class="h-full flex flex-col overflow-hidden">
    <div class="h-full overflow-y-scroll" bind:this={box}>
        <slot />
    </div>

    <div class="pagination" bind:this={paginationBox}>
        <button class="rounded-s-lg" disabled={currentPage == 1}
                on:click={() => { currentPage > 1 ? currentPage-- : currentPage = 1 }}>
            <span class="-rotate-90"><IconChevron /></span>
        </button>
        {#if ellipsis == "beginning" || ellipsis == "both"}
            <button disabled>…</button>
        {/if}
        {#each focusedPagesButtons as p}
            {@const page = p + 1}
            <button class:selected={currentPage == page} 
                    on:click={() => { currentPage = page }}>
                    {page}
            </button>
        {/each}
        {#if ellipsis == "end" || ellipsis == "both"}
            <button disabled>…</button>
        {/if}
        <button class="rounded-e-lg" disabled={currentPage == totalPages}
                on:click={() => { currentPage < totalPages ? currentPage++ : currentPage = totalPages }}>
            <span class="rotate-90"><IconChevron /></span>
        </button>
    </div>
</div>

<style>
    .pagination {
        @apply flex justify-center;
    }
    .pagination button {
        @apply h-8 w-8;
        @apply grid place-content-center;
        @apply text-a-gray-500 bg-white;
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