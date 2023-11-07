<script lang="ts">
  import { slide } from "svelte/transition"
  import cn from "classnames"

  import { afterNavigate } from "$app/navigation"

  import { clickOutside } from "$lib/helpers"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  export let showChevron = false
  export let placement = "right-0"

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
    class="flex items-center p-2 hover:text-orange"
    on:click={() => (isOpen = !isOpen)}
  >
    <slot name="title" />

    <ChevronDownIcon
      class={cn(
        "ml-0.5 h-4 w-4 transition duration-300",
        showChevron ? "inline" : "hidden",
        isOpen ? "rotate-180" : "rotate-0",
      )}
    />
  </button>
  {#if isOpen || isHover}
    <div class="absolute z-50 {placement}" transition:slide={{ duration: 200 }}>
      <slot />
    </div>
  {/if}
</div>
