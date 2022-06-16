<script lang="ts">
  import { _ } from "svelte-i18n";
  import { slide } from "svelte/transition";
  import ChevronUpIcon from "$components/icons/ChevronUpIcon.svelte";
  import ClearFilter from "$components/icons/ClearFilter.svelte";

  export let title: string;
  export let clearable = false;
  export let initExpanded = false;
</script>

<div
  class="-mx-2 pl-1 border-b border-gray-300 bg-lm-lightgray text-lm-dark hover:cursor-pointer"
>
  <div
    class="py-1.5 pr-2 relative flex justify-between"
    class:text-orange={clearable}
    class:collapsed={!initExpanded}
    on:click={() => (initExpanded = !initExpanded)}
  >
    <span class="pr-0">
      <ChevronUpIcon
        class="{initExpanded
          ? 'rotate-180'
          : ''} transition transition-duration-300 mr-1 h-3 w-3 inline rounded"
      />
      {$_(title)}
    </span>
    {#if clearable}
      <ClearFilter on:click />
    {/if}
  </div>
  {#if initExpanded}
    <div
      transition:slide={{ duration: 200 }}
      class={`shadow-inner bg-lm-light -ml-[0.5em] pl-2 ${initExpanded ? "py-2" : ""}`}
    >
      <slot />
    </div>
  {/if}
</div>
