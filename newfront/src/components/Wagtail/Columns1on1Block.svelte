<script lang="ts">
  import { blockMap } from "$components/Wagtail/utils";
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail";

  export let value: {
    left_column: WagtailStreamfieldBlock[];
    right_column: WagtailStreamfieldBlock[];
  } = { left_column: [], right_column: [] };
</script>

<div class="grid gap-8 mb-8 lg:grid-cols-2">
  <div>
    {#each value.left_column as block}
      <svelte:component this={blockMap[block.type]} bind:value={block.value} />
    {/each}
  </div>
  <div>
    {#each value.right_column as block}
      <svelte:component this={blockMap[block.type]} bind:value={block.value} />
    {/each}
  </div>
</div>
