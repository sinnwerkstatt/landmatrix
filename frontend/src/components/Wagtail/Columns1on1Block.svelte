<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import { blockMap } from "$components/Wagtail/blocks"

  export let value: {
    left_column: WagtailStreamfieldBlock[]
    right_column: WagtailStreamfieldBlock[]
  } = { left_column: [], right_column: [] }
</script>

<div data-block="columns_1_1" class="mb-8 grid gap-20 lg:grid-cols-2">
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
