<script lang="ts">
    import { openedFilterBar } from "$lib/accountability/stores"

    import Sidebar from "./atomic/Sidebar.svelte"
    import IconCollapse from "$components/Accountability/icons/IconCollapse.svelte"
</script>

{#if $openedFilterBar}
    <Sidebar>
        <div class="flex flex-nowrap justify-between">
            <span>Hullo</span>
            <button on:click={() => { $openedFilterBar = false }}>
                <IconCollapse />
            </button>
        </div>
        Hullo :D
    </Sidebar>
{/if}