<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import { blockMap } from "$components/Wagtail/blocks"

  export let value: {
    content: WagtailStreamfieldBlock[]
    color?: string
  }

  let customcol = value.color === "darkgrey" ? "bg-[#eee]" : ""
</script>

<div data-block="full_width_container" class="p-4 {customcol}">
  {#each value.content as block}
    <svelte:component this={blockMap[block.type]} bind:value={block.value} />
  {/each}
</div>
