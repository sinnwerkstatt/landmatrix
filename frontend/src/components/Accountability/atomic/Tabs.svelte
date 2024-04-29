<script lang="ts">
    import type { SvelteComponent } from "svelte"

    export let items: {label: string, value: number, component: SvelteComponent}[] = []
    export let activeTabValue = 1

    const handleClick = tabValue => () => (activeTabValue = tabValue)
</script>

<div class="h-full flex flex-col">
    <ul class="flex justify-center gap-1">
        {#each items as item}
            <li class={activeTabValue === item.value ? 'active' : ''}>
                <button on:click={handleClick(item.value)}>{item.label}</button>
            </li>
        {/each}
    </ul>
    
    {#each items as item}
        {#if activeTabValue == item.value}
            <div class="h-full overflow-x-auto overflow-y-hidden pt-2 flex flex-col gap-2">
                <svelte:component this={item.component} />
            </div>
        {/if}
    {/each}
</div>

<style>
    button {
        @apply w-fit;
        @apply px-[0.63rem] py-[0.44rem];
        @apply text-a-sm text-a-gray-400;
        @apply border border-a-gray-200 rounded-lg;
        @apply bg-white;
    }
    button:hover {
        @apply cursor-pointer;
        @apply text-a-gray-900 bg-a-gray-200;
    }
    li.active > button {
        @apply text-white bg-a-gray-900 border-a-gray-900;
    }
</style>