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
  class="border-b border-gray-300 bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-white"
>
  <div class="flex w-full" class:text-orange={clearable}>
    <button
      class="m-0.5 flex-grow p-1 text-left"
      on:click={() => (expanded = !expanded)}
    >
      <ChevronDownIcon
        class="transition-duration-300 inline h-4 w-4 rounded transition-transform {expanded
          ? 'rotate-180'
          : ''}"
      />
      {title}
    </button>
    {#if clearable}
      <button
        class="m-0.5 p-1"
        on:click={() => {
          expanded = false
          dispatch("clear")
        }}
      >
        <ClearFilter />
      </button>
    {/if}
  </div>
  {#if expanded}
    <div
      transition:slide={{ duration: 200 }}
      class="p-2 shadow-inner"
      bind:this={expandedContent}
    >
      <slot />
    </div>
  {/if}
</div>
