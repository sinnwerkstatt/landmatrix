<script lang="ts">
  import Siema from "siema"
  import { onMount } from "svelte"

  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"

  export let value

  let siema: Siema
  onMount(() => {
    siema = new Siema()
  })
</script>

<div data-block="slider" class="siema">
  {#each value.images as image}
    <ImageBlock value={image} />
  {/each}
</div>
