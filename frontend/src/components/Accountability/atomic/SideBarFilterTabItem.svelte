<script lang="ts">
    import { slide } from "svelte/transition"

    import BubbleCount from "./BubbleCount.svelte"
    import IconPlus from "../icons/IconPlus.svelte"
    import IconMinus from "../icons/IconMinus.svelte"
    import IconLockClosed from "../icons/IconLockClosed.svelte"

    export let label = "Label"
    export let open = false
    export let locked = false
    export let notification = false
    export let count = 0
</script>

<div class="bg-white border-b-2 border-a-gray-200">
    <div class="header">
        <div class:locked class="flex flex-nowrap gap-2 items-center">
            {#if locked}
                <IconLockClosed />
            {/if}
            <span class="line-clamp-1">{label}</span>
        </div>
        <div class="flex flex-nowrap gap-2 items-center">
            {#if count > 0}
                <BubbleCount {count} />
            {:else if notification}
                <div class="w-4 h-4 bg-a-primary-500 rounded-lg"></div>
            {/if}
            <button class="text-a-gray-400" on:click={() => { open = !open }}>
                {#if open}
                    <IconMinus />
                {:else}
                    <IconPlus />
                {/if}
            </button>
        </div>
    </div>

    {#if open}
        <div class="relative mb-4" transition:slide>
            <slot />
        </div>
    {/if}
</div>

<style>
    .header {
        @apply flex items-center justify-between gap-2;
        @apply px-4;
        @apply h-14 w-full;
        @apply shrink-0;
        @apply text-a-sm text-left font-medium;
    }
    .header .locked {
        @apply text-a-gray-400;
    }
</style>