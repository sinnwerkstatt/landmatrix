<script lang="ts">
  import { browser } from "$app/environment"

  import { lightboxImage } from "$lib/stores/basics"

  const onKeydown = (e: KeyboardEvent) => e.key === "Escape" && lightboxImage.set(null)
  const onClick = () => lightboxImage.set(null)

  $: if (browser) {
    if ($lightboxImage) {
      document.addEventListener("keydown", onKeydown)
      document.addEventListener("click", onClick)
    } else {
      document.removeEventListener("keydown", onKeydown)
      document.removeEventListener("click", onClick)
    }
  }
</script>

{#if $lightboxImage}
  <div
    class="fixed inset-0 z-[100] flex h-screen w-screen items-center justify-center bg-gray-600 bg-opacity-90 p-2"
  >
    <img
      class="max-h-full max-w-full border"
      src={$lightboxImage.image.url}
      alt={$lightboxImage.url}
      loading="lazy"
    />
  </div>
{/if}
