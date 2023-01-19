<script lang="ts">
  import type { BlockImage } from "$lib/types/custom"

  export let value: BlockImage

  $: link = value.image ? value.url : null
  $: src = value.image ? value.image.url : value.url
  $: caption = value.image ? value.caption : null
  $: externalLink = value.image ? value.external : false

  function escape_key(e) {
    if (e.key === "Escape") toggleLightbox()
  }
  let lightboxVisible = false
  function toggleLightbox() {
    if (lightboxVisible) {
      lightboxVisible = false
      document.removeEventListener("keydown", escape_key)
    } else {
      lightboxVisible = true
      document.addEventListener("keydown", escape_key)
    }
  }
</script>

<div data-block="image" class="mb-5">
  {#if value.lightbox}
    <a href={src} target="_blank" on:click|preventDefault={toggleLightbox}>
      <img class="w-full max-w-full cursor-pointer" {src} alt="" />
    </a>
  {:else if link}
    <a href={link} target={externalLink ? "_blank" : "_self"}>
      <img class="w-full max-w-full" {src} alt="" />
    </a>
  {:else}
    <img class="w-full max-w-full" {src} alt="" />
  {/if}
  {#if caption}
    <div class="caption bg-[rgba(0,0,0,.75)] p-3 font-bold text-orange">
      {@html caption}
    </div>
  {/if}
</div>

{#if lightboxVisible}
  <div
    class="fixed inset-0 z-[20000] flex h-screen w-screen items-center justify-center bg-gray-600 bg-opacity-90 p-2"
    on:click={toggleLightbox}
  >
    <img on:click|stopPropagation class="max-h-full max-w-full border" {src} alt="" />
  </div>
{/if}

<style>
  :global(.caption > *) {
    margin: 0 !important;
  }
</style>
