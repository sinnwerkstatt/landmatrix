<script lang="ts">
  import { lightboxImage } from "$lib/stores"
</script>

{#if $lightboxImage}
  <div
    class="fixed inset-0 z-[20000] flex h-screen w-screen items-center justify-center bg-gray-600 bg-opacity-90 p-2"
    on:click|preventDefault={() => lightboxImage.set(null)}
    on:keydown|preventDefault={e => e.key === "Escape" && lightboxImage.set(null)}
  >
    <img class="max-h-full max-w-full border" src={$lightboxImage.image.url} alt="" />
  </div>
{/if}
