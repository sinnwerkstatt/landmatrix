<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import Block from "$components/Wagtail/Block.svelte"

  interface Props {
    value: {
      content: WagtailStreamfieldBlock[]
      color?: "white" | "lightgrey" | "darkgrey"
    }
  }

  let { value }: Props = $props()

  const colorMap = {
    white: "bg-white dark:bg-gray-800",
    lightgrey: "bg-gray-50 dark:bg-gray-600",
    darkgrey: "bg-gray-100 dark:bg-gray-700",
  }
</script>

<div
  data-block="full_width_container"
  class="p-4 {value.color ? colorMap[value.color] : ''}"
>
  {#each value.content as block}
    <Block {block} />
  {/each}
</div>
