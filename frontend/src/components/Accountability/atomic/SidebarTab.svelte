<script lang="ts">
    import { createEventDispatcher } from "svelte"

    import { page } from "$app/stores"

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
    export let menuPosition = "auto"

    function showMenu() {
        if (menuPosition == "auto") {
            const y = box.getBoundingClientRect().y
            const height = box.getBoundingClientRect().height
            const center = y + height / 2
            position = center < window.innerHeight * 0.6 ? "bottom" : "top"
        } else {
            position = menuPosition
        }
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

    function writePath(id) {
        if (id) {
            return `/accountability/deals/${id}/`
        } else {
            return `/accountability/deals/0/`
        }
    }

    $: path = writePath(id)
    
</script>

<div class="relative">
    <div class="wrapper {state}" class:active={$page.url.pathname.startsWith(path)} bind:this={box} >
            <div class="flex items-center gap-2 w-full h-full">
                {#if handle}
                    <span class="shrink-0 cursor-move" draggable="true"><IconMove /></span>
                {/if}
                <a class="!text-a-gray-900 !text-a-sm w-full h-full grid items-center" href={path} >{label}</a>
            </div>
            {#if menu}
                <button class="text-a-gray-400" on:click={showMenu}><IconEllipsis /></button>
            {/if}
    </div>

    <div class="menu absolute {position} right-0 z-20">
        <DropdownMenu bind:visible={visibleMenu} >
            <DropdownMenuItem icon="check" on:click={handleEdit}>Edit</DropdownMenuItem>
            <DropdownMenuItem icon="bookmark" on:click={handleBookmark}>Unbookmark</DropdownMenuItem>
        </DropdownMenu>
    </div>
</div>


<style>
    .wrapper {
        @apply flex items-center justify-between gap-2;
        @apply px-4;
        @apply h-14 w-full;
        @apply shrink-0;
        @apply text-a-sm text-left font-medium;
        @apply bg-white;
        @apply border-b-2 border-a-gray-200;
    }
    .wrapper:hover,
    .wrapper.active {
        @apply bg-a-gray-100;
        @apply border-transparent rounded-lg;
    }

    .menu.top {
        @apply -top-[4rem];
    }

    .menu.bottom {
        @apply top-12;
    }
</style>