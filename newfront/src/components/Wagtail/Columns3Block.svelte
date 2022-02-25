<script lang="ts">
  import { blockMap } from "$components/Wagtail/utils";
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail";

  export let value: {
    left_column: WagtailStreamfieldBlock[];
    middle_column: WagtailStreamfieldBlock[];
    right_column: WagtailStreamfieldBlock[];
  };
</script>

<div class="grid gap-4 mb-8 lg:grid-cols-3">
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
