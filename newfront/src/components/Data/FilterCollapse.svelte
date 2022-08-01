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
  class="-mx-2 pl-1 border-b border-gray-300 bg-lm-lightgray text-lm-dark hover:cursor-pointer"
>
  <div
    class="py-1.5 pr-2 relative flex justify-between"
    class:text-orange={clearable}
    class:collapsed={!expanded}
    on:click={() => (expanded = !expanded)}
  >
    <span class="pr-0">
      <ChevronDownIcon
        class="transition-transform transition-duration-300 mr-1 h-4 w-4 inline rounded {expanded
          ? 'rotate-180'
          : ''}"
      />
      {$_(title)}
    </span>
    {#if clearable}
      <ClearFilter on:click />
    {/if}
  </div>
  {#if expanded}
    <div
      transition:slide={{ duration: 200 }}
      class="shadow-inner bg-lm-light -ml-[0.5em] p-2"
    >
      <slot />
    </div>
  {/if}
</div>
