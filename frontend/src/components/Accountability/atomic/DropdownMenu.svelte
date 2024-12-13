<script lang="ts">
  import { fade } from "svelte/transition"

  import { clickOutside } from "$lib/accountability/clickOutside"

  export let visible = false
  export let extraClass = ""

  export let top = 0
  export let left = 0

  function handleClickOutside() {
    visible = false
  }
</script>

{#if visible}
  <div
    class="{extraClass} flex flex-col rounded-lg border border-a-gray-200 bg-white shadow-a-md"
    style="top:{top}px; left:{left}px;"
    use:clickOutside
    on:clickoutside={handleClickOutside}
    in:fade={{ duration: 150 }}
  >
    <slot />
  </div>
{/if}
