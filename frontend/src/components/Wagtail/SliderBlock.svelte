<script lang="ts">
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"

  export let value
</script>

<div data-block="slider" class="siema mx-auto max-h-[800px] w-full max-w-[600px]">
  {#each value.images as image}
    <ImageBlock value={image} />
  {/each}
</div>
