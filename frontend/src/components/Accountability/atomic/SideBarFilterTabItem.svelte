<script lang="ts">
  import { slide } from "svelte/transition"

  import IconLockClosed from "../icons/IconLockClosed.svelte"
  import IconMinus from "../icons/IconMinus.svelte"
  import IconPlus from "../icons/IconPlus.svelte"
  import BubbleCount from "./BubbleCount.svelte"

  interface Props {
    label?: string
    open?: boolean
    locked?: boolean
    notification?: boolean
    count?: number
    children?: import("svelte").Snippet
  }

  let {
    label = "Label",
    open = $bindable(false),
    locked = false,
    notification = false,
    count = 0,
    children,
  }: Props = $props()
</script>

<div class="border-b-2 border-a-gray-200 bg-white">
  <div class="header">
    <div class:locked class="flex flex-nowrap items-center gap-2">
      {#if locked}
        <IconLockClosed />
      {/if}
      <span class="line-clamp-1">{label}</span>
    </div>
    <div class="flex flex-nowrap items-center gap-2">
      {#if count > 0}
        <BubbleCount {count} />
      {:else if notification}
        <div class="h-4 w-4 rounded-lg bg-a-primary-500"></div>
      {/if}
      <button
        class="text-a-gray-400"
        onclick={() => {
          open = !open
        }}
      >
        {#if open}
          <IconMinus />
        {:else}
          <IconPlus />
        {/if}
      </button>
    </div>
  </div>

  {#if open}
    <div class="relative mb-4" transition:slide>
      {@render children?.()}
    </div>
  {/if}
</div>

<style>
  .header {
    @apply flex items-center justify-between gap-2;
    @apply px-4;
    @apply h-14 w-full;
    @apply shrink-0;
    @apply text-left text-a-sm font-medium;
  }
  .header .locked {
    @apply text-a-gray-400;
  }
</style>
