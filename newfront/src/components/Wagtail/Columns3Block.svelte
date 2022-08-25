<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail";
  import { blockMap } from "$components/Wagtail/blocks";

  export let value: {
    left_column: WagtailStreamfieldBlock[];
    middle_column: WagtailStreamfieldBlock[];
    right_column: WagtailStreamfieldBlock[];
  };
</script>

<div data-block="columns_3" class="mb-8 grid gap-4 lg:grid-cols-3">
  <div>
    {#each value.left_column as block}
      <svelte:component this={blockMap[block.type]} bind:value={block.value} />
    {/each}
  </div>
  <div>
    {#each value.middle_column as block}
      <svelte:component this={blockMap[block.type]} bind:value={block.value} />
    {/each}
  </div>
  <div>
    {#each value.right_column as block}
      <svelte:component this={blockMap[block.type]} bind:value={block.value} />
    {/each}
  </div>
</div>
