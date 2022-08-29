<script lang="ts">
  import { _ } from "svelte-i18n";
  import { slide } from "svelte/transition";
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte";
  import ClearFilter from "$components/icons/ClearFilter.svelte";

  export let title: string;
  export let clearable = false;
  export let expanded = false;
</script>

<div
  class="-mx-2 border-b border-gray-300 bg-lm-lightgray pl-1 text-lm-dark hover:cursor-pointer"
>
  <div
    class="relative flex justify-between py-1.5 pr-2"
    class:text-orange={clearable}
    class:collapsed={!expanded}
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
  </div>
  {#if expanded}
    <div
      transition:slide={{ duration: 200 }}
      class="-ml-[0.5em] bg-lm-light p-2 shadow-inner"
    >
      <slot />
    </div>
  {/if}
</div>
