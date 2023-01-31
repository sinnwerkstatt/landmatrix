<script lang="ts">
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"

  export let value
</script>

<div data-block="slider" class="mx-auto w-full">
  {#each value.images as image}
    <ImageBlock value={image} />
  {/each}
</div>
