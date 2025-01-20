<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import Block from "$components/Wagtail/Block.svelte"

  interface Props {
    value?: {
      left_column: WagtailStreamfieldBlock[]
      right_column: WagtailStreamfieldBlock[]
    }
  }

  let { value = { left_column: [], right_column: [] } }: Props = $props()
</script>

<div class="mb-8 grid grid-cols-1 gap-20 lg:grid-cols-2" data-block="columns_1_1">
  <div>
    {#each value.left_column as block}
      <Block {block} />
    {/each}
  </div>
  <div>
    {#each value.right_column as block}
      <Block {block} />
    {/each}
  </div>
</div>
