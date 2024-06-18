<script lang="ts">
  import { lightboxImage } from "$lib/stores/basics"
  import type { BlockImage } from "$lib/types/wagtail"

  export let value: BlockImage

  $: link = value.image ? value.url : null
  $: src = value.image ? value.image.url : value.url
  $: caption = value.image ? value.caption : null
  $: externalLink = value.image ? value.external : false
</script>

<div data-block="image" class="mb-5">
  {#if value.lightbox}
    <a
      href={src}
      on:click|preventDefault|stopPropagation={() => lightboxImage.set(value)}
      on:keydown|preventDefault|stopPropagation={e =>
        e.code === "Enter" && lightboxImage.set(value)}
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
