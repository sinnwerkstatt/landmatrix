<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import { blockMap } from "$components/Wagtail/blocks"

  export let value: {
    content: WagtailStreamfieldBlock[]
    color?: "white" | "lightgrey" | "darkgrey"
  }

  const colorMap = {
    white: "bg-white dark:bg-gray-800",
    lightgrey: "bg-lm-lightgray dark:bg-gray-600",
    darkgrey: "bg-lm-darkgray dark:bg-gray-700",
  }
</script>

<div
  data-block="full_width_container"
  class="p-4 {value.color ? colorMap[value.color] : ''}"
>
  {#each value.content as block}
    <svelte:component this={blockMap[block.type]} bind:value={block.value} />
  {/each}
</div>
