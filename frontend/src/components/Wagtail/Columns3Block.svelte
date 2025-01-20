<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import Block from "$components/Wagtail/Block.svelte"

  interface Props {
    value: {
      left_column: WagtailStreamfieldBlock[]
      middle_column: WagtailStreamfieldBlock[]
      right_column: WagtailStreamfieldBlock[]
    }
  }

  let { value }: Props = $props()
</script>

<div
  class="mx-auto mb-8 grid max-w-[1200px] grid-cols-1 lg:grid-cols-3"
  data-block="columns_3"
>
  <div>
    {#each value.left_column as block}
      <Block {block} />
    {/each}
  </div>
  <div>
    {#each value.middle_column as block}
      <Block {block} />
    {/each}
  </div>
  <div>
    {#each value.right_column as block}
      <Block {block} />
    {/each}
  </div>
</div>
