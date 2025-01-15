<script lang="ts">
  import { page } from "$app/state"

  import { filters, FilterValues } from "$lib/accountability/filters"
  import { openProjectModal } from "$lib/accountability/projects"
  import { openedFilterBar } from "$lib/accountability/stores"

  import IconCollapse from "$components/Accountability/icons/IconCollapse.svelte"

  import Filters from "./atomic/Filters.svelte"
  import Sidebar from "./atomic/Sidebar.svelte"
  import Button from "./Button.svelte"
</script>

{#if $openedFilterBar}
  <Sidebar>
    <div class="flex flex-nowrap items-center justify-between">
      <span class="text-a-sm font-semibold text-a-gray-500">Filters</span>
      <button
        onclick={() => {
          $openedFilterBar = false
        }}
      >
        <IconCollapse />
      </button>
    </div>

    <Filters />

    <div class="flex flex-wrap justify-center gap-2 px-2">
      <Button
        label="Save new project"
        size="sm"
        style="neutral"
        onclick={() => openProjectModal("create")}
      />
      <Button
        label="Clear all"
        size="sm"
        style="neutral"
        type="outline"
        onclick={() => ($filters = new FilterValues(page.data.project.filters))}
      />
      <!-- {#if $page.data.project.owner == $me?.id}
                <Button label="Update" size="sm" style="neutral" on:click={() => openSaveModal("update")} />
            {/if} -->
      <!-- <Button label="Clear all" size="sm" style="neutral" type="outline" on:click={() => $filters = $filters.empty()} /> -->
    </div>
  </Sidebar>
{/if}
