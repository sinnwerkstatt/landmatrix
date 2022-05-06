<script lang="ts">
  import VirtualList from "@sveltejs/svelte-virtual-list";
  import { deals } from "$lib/data";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
</script>

<DataContainer>
  <div class="h-full flex">
    <div
      class="flex-none h-full min-h-[3px] {$showFilterBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />

    <div class="p-4 bg-green-300 w-full">
      {$deals?.length}
      <VirtualList items={$deals ?? []} let:item>
        <p><a href="/deal/{item.id}">{item.id}: {item.country.name}</a></p>
      </VirtualList>
    </div>
    <div
      class="flex-none h-full min-h-[3px] {$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />
  </div>
</DataContainer>
