<!-- @migration-task Error while migrating Svelte code: This migration would change the name of a slot making the component unusable -->
<script lang="ts">
  import Pagination from "./Pagination.svelte"

  export let data: [] = []
  export let pageContent = [] // Data that should be displayed in this specific page (pagination)
  export let filters = true

  let container: HTMLElement

  // Styling
  export let rowHeight = 56

  let rowsByPage: number
  let tableHeight = "132"

  let pagination

  $: tableHeight = (rowsByPage * rowHeight + 34).toString()
</script>

<div class="flex h-full flex-col">
  <!-- Filters -->
  {#if filters}
    <div class="rounded-t-lg border-x border-t bg-white p-4">
      <slot name="filters" />
    </div>
  {/if}

  <!-- Table container for height calculation -->
  <div class="grow" bind:this={container}>
    <div class="flex flex-col overflow-auto border-x" style="height: {tableHeight}px;">
      <!-- Header -->
      <div class={filters ? "" : "overflox-clip rounded-t-lg border-t"}>
        <slot name="header" />
        <!-- <svelte:fragment slot="header"></svelte:fragment> ADD TABLE ROW IN THIS -->
      </div>

      <!-- Body -->
      <div class="grow">
        <slot name="body" />
        <!-- <svelte:fragment slot="body"></svelte:fragment> ADD TABLE ROW IN THIS -->
      </div>
    </div>

    <div
      class="flex min-h-16 justify-between rounded-b-lg border-x border-b bg-white p-4"
    >
      <div class="text-a-sm font-normal text-a-gray-500">
        Showing
        <span class="font-medium text-a-gray-900">
          {pagination?.first}-{pagination?.last}
        </span>
        of
        <span class="font-medium text-a-gray-900">{pagination?.total}</span>
      </div>
      <div class="w-40 md:w-96">
        <Pagination
          detached={true}
          bind:box={container}
          bind:dataset={data}
          bind:pageContent
          bind:rowsByPage
          {rowHeight}
          bind:pagination
          justify="end"
        />
      </div>
    </div>
  </div>
</div>
