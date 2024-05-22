<script lang="ts">
    import { page } from "$app/stores"
    import { slide } from "svelte/transition"
    import { quintOut } from 'svelte/easing'
    import { openedFilterBar } from "$lib/accountability/stores"

    import IconExpand from "$components/Accountability/icons/IconExpand.svelte"

    $: project_id = $page.params.project
</script>

<div class="py-4 flex gap-4">
    {#if !$openedFilterBar}
        <button on:click={() => { $openedFilterBar = true }}
                in:slide={{ duration: 800, easing: quintOut, axis: 'x' }}
                out:slide={{ duration: 200, easing: quintOut, axis: 'x' }} >
            <IconExpand />
        </button>
    {/if}
    <div>
        <h1 class="text-a-3xl font-semibold">
            {#if project_id == 0}
                All deals
            {:else}
                Project {project_id}
            {/if}
        </h1>
        <p class="text-a-gray-500 font-normal">All deals from the database.</p>
    </div>
</div>