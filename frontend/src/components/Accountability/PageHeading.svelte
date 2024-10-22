<script lang="ts">
  import { quintOut } from "svelte/easing"
  import { slide } from "svelte/transition"

  import { page } from "$app/stores"

  import { openedFilterBar } from "$lib/accountability/stores"

  import IconExpand from "$components/Accountability/icons/IconExpand.svelte"

  $: project_id = $page.params.project
</script>

<div class="flex gap-4 py-4">
  {#if !$openedFilterBar}
    <button
      on:click={() => {
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
      {#if project_id == 0}
        All deals
      {:else}
        Project {project_id}
      {/if}
    </h1>
    <p class="font-normal text-a-gray-500">All deals from the database.</p>
  </div>
</div>
