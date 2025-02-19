<script lang="ts">
  import { type Snippet } from "svelte"
  import { slide } from "svelte/transition"

  import ContextHelper from "$components/ContextHelper.svelte"
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import ClearFilter from "$components/icons/ClearFilter.svelte"

  interface Props {
    title: string
    clearable?: boolean
    expanded?: boolean
    contextHelp?: string
    children: Snippet
    onclear?: () => void
    onExpanded?: () => void
  }

  let {
    title,
    clearable = false,
    expanded = false,
    contextHelp,
    children,
    onclear,
    onExpanded,
  }: Props = $props()

  let expandedContent: HTMLDivElement | undefined = $state()
  $effect(() => {
    if (expandedContent) onExpanded?.()
  })
</script>

<div
  class="border-b border-gray-300 bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-white"
>
  <div class="flex w-full" class:text-orange={clearable}>
    <div class="flex flex-grow items-center gap-1">
      <button
        class="m-0.5 flex items-center gap-1 p-1 text-left"
        onclick={() => (expanded = !expanded)}
        type="button"
      >
        <ChevronDownIcon
          class="transition-duration-300 inline h-4 w-4 rounded transition-transform {expanded
            ? 'rotate-180'
            : ''}"
        />
        {title}
      </button>
      {#if contextHelp}
        <ContextHelper identifier={contextHelp} class="size-4" />
      {/if}
      <button
        class="h-full flex-grow"
        onclick={() => (expanded = !expanded)}
        type="button"
        aria-label="toggle menu"
      ></button>
    </div>
    {#if clearable}
      <button
        class="m-0.5 p-1"
        onclick={() => {
          expanded = false
          onclear?.()
        }}
        type="reset"
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
      {@render children()}
    </div>
  {/if}
</div>
