<script lang="ts">
  import type { WagtailStreamfieldBlock } from "$lib/types/wagtail"

  import Block from "$components/Wagtail/Block.svelte"

  interface Props {
    content?: WagtailStreamfieldBlock[]
    class?: string
  }

  let { content = [], class: className = "" }: Props = $props()
</script>

<div class="container mx-auto pb-0 pt-6 {className}">
  {#each content as block}
    <Block {block} />
  {/each}
</div>
