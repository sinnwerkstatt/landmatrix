<script lang="ts">
  import { slide } from "svelte/transition"

  import IconChevron from "../icons/IconChevron.svelte"
  import IconChevronSort from "../icons/IconChevronSort.svelte"

  interface Props {
    title?: string
    stickyTitle?: boolean
    alwaysOpen?: boolean // Create a section that can't be closed
    sortable?: boolean
    open?: boolean
    extraClass?: string
    children?: import("svelte").Snippet
    onSort?: () => void
  }

  let {
    title = "Title",
    stickyTitle = false,
    alwaysOpen = false,
    sortable = false,
    open = $bindable(true),
    extraClass = "",
    children,
    onSort,
  }: Props = $props()

  function handleClick() {
    if (!alwaysOpen) open = !open
  }
</script>

<div class="flex h-fit min-h-16 flex-col" class:stickyTitle>
  <button
    class="flex w-full shrink-0 items-center justify-between bg-white px-4 pb-2 pt-4 font-semibold {extraClass}"
    onclick={handleClick}
  >
    <div class="flex items-center">
      {title}
      {#if !alwaysOpen}
        <span class:open class="chevron"><IconChevron /></span>
      {/if}
    </div>

    {#if sortable}
      <!-- svelte-ignore node_invalid_placement_ssr -->
      <button class="flex items-center text-a-gray-500" onclick={onSort}>
        A-Z <IconChevronSort />
      </button>
    {/if}
  </button>

  {#if alwaysOpen || open}
    <div
      class="relative flex h-full flex-col gap-2 overflow-auto pb-2"
      transition:slide
    >
      {@render children?.()}
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
