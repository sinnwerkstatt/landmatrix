<script lang="ts">
  import type { BlockImage } from "$lib/types/wagtail"

  import ImageBlock from "$components/Wagtail/ImageBlock.svelte"

  interface Props {
    value: {
      images: BlockImage[]
      columns: number
    }
  }

  let { value }: Props = $props()

  const cols_map = { 3: "grid-cols-3", 5: "grid-cols-5" }
  let galleryColumns = $derived(cols_map[value.columns] ?? "grid-cols-1")
</script>

<div data-block="gallery" class="grid gap-4 {galleryColumns}">
  {#each value.images as image}
    <div class="col">
      <ImageBlock value={image} />
    </div>
  {/each}
</div>
