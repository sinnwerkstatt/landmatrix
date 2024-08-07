<script lang="ts">
    import { openedFilterBar } from "$lib/accountability/stores"
    import { openProjectModal } from "$lib/accountability/projects"
    import { filters, FilterValues } from "$lib/accountability/filters"
    import { page } from "$app/stores"

    import Sidebar from "./atomic/Sidebar.svelte"
    import Filters from "./atomic/Filters.svelte"
    import Button from "./Button.svelte"
    import IconCollapse from "$components/Accountability/icons/IconCollapse.svelte"
 
</script>

{#if $openedFilterBar}
    <Sidebar>
        <div class="flex items-center flex-nowrap justify-between">
            <span class="text-a-sm font-semibold text-a-gray-500">Filters</span>
            <button on:click={() => { $openedFilterBar = false }}>
                <IconCollapse />
            </button>
        </div>

        <Filters />

        <div class="px-2 flex justify-center gap-2 flex-wrap">
            <Button label="Save new project" size="sm" style="neutral" on:click={() => openProjectModal('create')} />
            <Button label="Clear all" size="sm" style="neutral" type="outline" on:click={() => $filters = new FilterValues($page.data.project.filters)} />
            <!-- {#if $page.data.project.owner == $me.id}
                <Button label="Update" size="sm" style="neutral" on:click={() => openSaveModal("update")} />
            {/if} -->
            <!-- <Button label="Clear all" size="sm" style="neutral" type="outline" on:click={() => $filters = $filters.empty()} /> -->
        </div>
    </Sidebar>
{/if}
