<script lang="ts">
    import { slide } from "svelte/transition"
    import { quintOut } from 'svelte/easing'
    import { openedFilterBar } from "$lib/accountability/stores"

    import IconExpand from "$components/Accountability/icons/IconExpand.svelte"
</script>

<div class="p-4 flex gap-4">
    {#if !$openedFilterBar}
        <button on:click={() => { $openedFilterBar = true }}
                in:slide={{ duration: 800, easing: quintOut, axis: 'x' }}
                out:slide={{ duration: 200, easing: quintOut, axis: 'x' }} >
            <IconExpand />
        </button>
    {/if}
    <div>
        <h1 class="text-a-3xl font-semibold">Hullo</h1>
        <p class="text-a-gray-500 font-normal">All deals from the database.</p>
    </div>
</div>