<script lang="ts">
    import { slide } from "svelte/transition"
    import { createEventDispatcher } from "svelte"

    import IconChevron from "../icons/IconChevron.svelte"
    import IconChevronSort from "../icons/IconChevronSort.svelte"

    const dispatch = createEventDispatcher()

    export let title = "Title"
    export let stickyTitle = false
    export let alwaysOpen = false // Create a section that can't be closed
    export let sortable = false
    export let open = true

    function handleClick() { if (!alwaysOpen) open = !open }

    function autoSort() { dispatch('sort') }
</script>

<div class="flex flex-col h-fit" class:stickyTitle >
    <button class="flex items-center justify-between w-full px-4 pt-4 pb-2 font-semibold shrink-0 bg-white" on:click={handleClick}>
        <div class="flex items-center">
            {title}
            {#if !alwaysOpen}
                <span class:open class="chevron"><IconChevron /></span>
            {/if}
        </div>

        {#if sortable}
            <button class="flex items-center text-a-gray-500" on:click={autoSort}>A-Z <IconChevronSort /></button>
        {/if}
    </button>
    
    {#if alwaysOpen || open}
        <div class="flex flex-col gap-2 h-full overflow-auto" transition:slide>
            <slot />
        </div>
    {/if}
</div>

<style>
    .chevron {  
        @apply rotate-180;
    }
    .chevron.open {
        @apply rotate-0;
    }
    .stickyTitle {
        /* @apply sticky top-0 z-10; */
        @apply h-full;
    }
</style>