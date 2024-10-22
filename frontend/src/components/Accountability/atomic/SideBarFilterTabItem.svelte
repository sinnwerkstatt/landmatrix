<script lang="ts">
  import { slide } from "svelte/transition"

  import IconLockClosed from "../icons/IconLockClosed.svelte"
  import IconMinus from "../icons/IconMinus.svelte"
  import IconPlus from "../icons/IconPlus.svelte"
  import BubbleCount from "./BubbleCount.svelte"

  export let label = "Label"
  export let open = false
  export let locked = false
  export let notification = false
  export let count = 0
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
        on:click={() => {
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
      <slot />
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
