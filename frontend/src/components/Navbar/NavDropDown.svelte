<script lang="ts">
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"

  import { clickOutside } from "$lib/helpers"

  export let placement = "left-0"

  let isOpen = false
  let isHover = false

  afterNavigate(() => (isOpen = false))
</script>

<div
  role="none"
  class="relative {$$props.class ?? ''}"
  use:clickOutside
  on:outClick={() => (isOpen = false)}
  on:mouseenter={() => (isHover = true)}
  on:mouseleave={() => {
    isHover = false
    isOpen = false
  }}
>
  <button
    class="flex items-center hover:text-orange"
    on:click={() => (isOpen = !isOpen)}
  >
    <slot name="title" />
  </button>
  {#if isOpen || isHover}
    <div class="absolute z-50 {placement}" transition:slide={{ duration: 200 }}>
      <slot />
    </div>
  {/if}
</div>
