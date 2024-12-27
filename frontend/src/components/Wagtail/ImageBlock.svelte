<script lang="ts">
  import { lightboxImage } from "$lib/stores/basics"
  import type { BlockImage } from "$lib/types/wagtail"

  interface Props {
    value: BlockImage
  }

  let { value }: Props = $props()

  let link = $derived(value.image ? value.url : null)
  let src = $derived(value.image ? value.image.url : value.url)
  let caption = $derived(value.image ? value.caption : null)
  let externalLink = $derived(value.image ? value.external : false)
</script>

<div data-block="image" class="mb-5">
  {#if value.lightbox}
    <a
      href={src}
      onclick={e => {
        e.stopPropagation()
        e.preventDefault()
        lightboxImage.set(value)
      }}
      onkeydown={e => {
        e.stopPropagation()
        e.preventDefault()
        if (e.code === "Enter") lightboxImage.set(value)
      }}
    >
      <img class="w-full max-w-full cursor-pointer" {src} alt="" loading="lazy" />
    </a>
  {:else if link}
    <a
      href={link}
      target={externalLink ? "_blank" : "_self"}
      rel={externalLink ? "noreferrer" : ""}
    >
      <img class="w-full max-w-full" {src} alt="" loading="lazy" />
    </a>
  {:else}
    <img class="w-full max-w-full" {src} alt="" loading="lazy" />
  {/if}
  {#if caption}
    <div class="caption bg-[rgba(0,0,0,.75)] p-3 font-bold text-orange">
      {@html caption}
    </div>
  {/if}
</div>

<style lang="css">
  :global(.caption > *) {
    margin: 0 !important;
  }
</style>
