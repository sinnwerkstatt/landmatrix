<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { slide } from "svelte/transition"

  import IconChevron from "../icons/IconChevron.svelte"
  import IconChevronSort from "../icons/IconChevronSort.svelte"

  const dispatch = createEventDispatcher()

  export let title = "Title"
  export let stickyTitle = false
  export let alwaysOpen = false // Create a section that can't be closed
  export let sortable = false
  export let open = true
  export let extraClass = ""

  function handleClick() {
    if (!alwaysOpen) open = !open
  }

  function autoSort() {
    dispatch("sort")
  }
</script>

<div class="flex h-fit min-h-16 flex-col" class:stickyTitle>
  <button
    class="flex w-full shrink-0 items-center justify-between bg-white px-4 pb-2 pt-4 font-semibold {extraClass}"
    on:click={handleClick}
  >
    <div class="flex items-center">
      {title}
      {#if !alwaysOpen}
        <span class:open class="chevron"><IconChevron /></span>
      {/if}
    </div>

    {#if sortable}
      <button class="flex items-center text-a-gray-500" on:click={autoSort}>
        A-Z <IconChevronSort />
      </button>
    {/if}
  </button>

  {#if alwaysOpen || open}
    <div
      class="relative flex h-full flex-col gap-2 overflow-auto pb-2"
      transition:slide
    >
      <slot />
    </div>
  {/if}
</div>

<style>
  .chevron {
    @apply rotate-180;
  }
  .chevron.open {
    @apply rotate-0;
  }
  .stickyTitle {
    /* @apply sticky top-0 z-10; */
    @apply h-full;
  }
</style>
