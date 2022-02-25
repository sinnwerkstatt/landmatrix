<script lang="ts">
  import { blockMap } from "$components/Wagtail/blocks";
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail";

  export let value: {
    content: WagtailStreamfieldBlock[];
    color?: string;
  };

  let customcol = value.color === "darkgrey" ? "bg-[#eee]" : "";
</script>

<div class="p-4 {customcol}">
  {#each value.content as block}
    <svelte:component this={blockMap[block.type]} bind:value={block.value} />
  {/each}
</div>
