<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { slide } from "svelte/transition"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import ClearFilter from "$components/icons/ClearFilter.svelte"

  const dispatch = createEventDispatcher()

  export let title: string
  export let clearable = false
  export let expanded = false

  let expandedContent: HTMLDivElement | undefined
  $: if (expandedContent) dispatch("expanded")
</script>

<div
  class="-mx-2 border-b border-gray-300 bg-lm-lightgray pl-1 text-lm-dark dark:bg-gray-800 dark:text-white"
>
  <button
    class="flex w-full cursor-pointer justify-between py-1.5 pr-2"
    class:collapsed={!expanded}
    class:text-orange={clearable}
    on:click={() => (expanded = !expanded)}
  >
    <span class="pr-0">
      <ChevronDownIcon
        class="transition-duration-300 mr-1 inline h-4 w-4 rounded transition-transform {expanded
          ? 'rotate-180'
          : ''}"
      />
      {title}
    </span>
    {#if clearable}
      <ClearFilter on:click />
    {/if}
  </button>
  {#if expanded}
    <div
      transition:slide={{ duration: 200 }}
      class="-ml-[0.5em] p-2 shadow-inner"
      bind:this={expandedContent}
    >
      <slot />
    </div>
  {/if}
</div>
