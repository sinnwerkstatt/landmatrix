<script lang="ts">
    import { createEventDispatcher } from "svelte"

    import IconMove from "../icons/IconMove.svelte"
    import IconEllipsis from "../icons/IconEllipsis.svelte"
    import DropdownMenu from "./DropdownMenu.svelte"
    import DropdownMenuItem from "./DropdownMenuItem.svelte"

    const dispatch = createEventDispatcher()

    let box:HTMLElement
    let visibleMenu = false
    let position = "bottom"

    export let id:number
    export let label = "label"
    export let state = "default"
    export let menu = false
    export let handle = false
    export let active = false

    function showMenu() {
        const y = box.getBoundingClientRect().y
        const height = box.getBoundingClientRect().height
        const center = y + height / 2
        
        position = center < window.innerHeight * 0.6 ? "bottom" : "top"
        visibleMenu = true
    }

    function handleEdit() {
        dispatch('edit', { id })
        visibleMenu = false
    }

    function handleBookmark() {
        dispatch('bookmark', { id })
        visibleMenu = false
    }
    
</script>

<div class="relative">
    <button class="{state}" class:active bind:this={box} on:click={showMenu}>
            <div class="flex items-center gap-2">
                {#if handle}
                    <span class="shrink-0 cursor-move" draggable="true"><IconMove /></span>
                {/if}
                {label}
            </div>
            {#if menu}
                <span class="text-a-gray-400"><IconEllipsis /></span>
            {/if}
    </button>

    <div class="menu absolute {position} right-0 z-20">
        <DropdownMenu bind:visible={visibleMenu}>
            <DropdownMenuItem icon="check" on:click={handleEdit}>Edit</DropdownMenuItem>
            <DropdownMenuItem icon="bookmark" on:click={handleBookmark}>Unbookmark</DropdownMenuItem>
        </DropdownMenu>
    </div>
</div>


<style>
    button {
        @apply flex items-center justify-between gap-2;
        @apply px-4;
        @apply h-14 w-full;
        @apply shrink-0;
        @apply text-a-sm text-left font-medium;
        @apply bg-white;
        @apply border-b-2 border-a-gray-200;
    }
    button:hover,
    button.active {
        @apply bg-a-gray-100;
        @apply border-transparent rounded-lg;
    }

    .menu.top {
        @apply -top-[4.5rem];
    }
</style>