<script lang="ts">
  import type { BlockImage } from "$lib/types/custom";
  import ImageBlock from "$components/Wagtail/ImageBlock.svelte";

  export let value: {
    images: BlockImage[];
    columns: number;
  };

  const cols_map = { 3: "grid-cols-3", 5: "grid-cols-5" };
  $: galleryColumns = cols_map[value.columns] ?? "grid-cols-1";
</script>

<div data-block="gallery" class="grid gap-4 {galleryColumns}">
  {#each value.images as image}
    <div class="col">
      <ImageBlock value={image} />
    </div>
  {/each}
</div>
