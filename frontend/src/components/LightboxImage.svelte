<script lang="ts">
  import { lightboxImage } from "$lib/stores"

  const onKeydown = (e: KeyboardEvent) => e.key === "Escape" && lightboxImage.set(null)
  const onClick = () => lightboxImage.set(null)

  $: if ($lightboxImage) {
    document.addEventListener("keydown", onKeydown)
    document.addEventListener("click", onClick)
  } else {
    document.removeEventListener("keydown", onKeydown)
    document.removeEventListener("click", onClick)
  }
</script>

{#if $lightboxImage}
  <div
    class="fixed inset-0 z-[20000] flex h-screen w-screen items-center justify-center bg-gray-600 bg-opacity-90 p-2"
  >
    <img
      class="max-h-full max-w-full border"
      src={$lightboxImage.image.url}
      alt={$lightboxImage.url}
    />
  </div>
{/if}
