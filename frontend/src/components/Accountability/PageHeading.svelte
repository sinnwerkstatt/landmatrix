<script lang="ts">
  import { quintOut } from "svelte/easing"
  import { slide } from "svelte/transition"

  import { page } from "$app/state"

  import { openedFilterBar } from "$lib/accountability/stores"

  import IconExpand from "$components/Accountability/icons/IconExpand.svelte"

  let { data } = $props()

  let projectId = $derived(page.params.project)

  let currentProject = $derived(data.allProjects.find(p => p.id == projectId))
</script>

<div class="flex gap-4 py-4">
  {#if !$openedFilterBar}
    <button
      onclick={() => {
        $openedFilterBar = true
      }}
      in:slide={{ duration: 800, easing: quintOut, axis: "x" }}
      out:slide={{ duration: 200, easing: quintOut, axis: "x" }}
    >
      <IconExpand />
    </button>
  {/if}
  <div>
    <h1 class="text-a-3xl font-semibold">
      {#if projectId == 0}
        All deals
      {:else}
        {currentProject?.name ?? "Project"}
      {/if}
    </h1>
    <p class="font-normal text-a-gray-500">All deals from the database.</p>
  </div>
</div>
