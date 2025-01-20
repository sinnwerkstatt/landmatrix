<script lang="ts">
  import type { Snippet } from "svelte"
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"

  import { clickOutside } from "$lib/helpers"

  interface Props {
    placement?: string
    class?: string
    title?: Snippet
    children?: Snippet
  }

  let { placement = "left-0", class: className = "", title, children }: Props = $props()

  let isOpen = $state(false)
  let isHover = $state(false)

  afterNavigate(() => (isOpen = false))
</script>

<div
  role="none"
  class="relative {className}"
  use:clickOutside
  onoutClick={() => (isOpen = false)}
  onmouseenter={() => (isHover = true)}
  onmouseleave={() => {
    isHover = false
    isOpen = false
  }}
>
  <button
    class="flex items-center hover:text-orange"
    onclick={() => (isOpen = !isOpen)}
    type="button"
  >
    {@render title?.()}
  </button>
  {#if isOpen || isHover}
    <div class="absolute z-50 {placement}" transition:slide={{ duration: 200 }}>
      {@render children?.()}
    </div>
  {/if}
</div>
