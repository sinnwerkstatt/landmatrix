<script lang="ts">
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"

  let { value } = $props()
</script>

<div data-block="slider">
  {#if value.images.length}
    <ImageBlock value={value.images[0]} />
  {/if}
</div>
