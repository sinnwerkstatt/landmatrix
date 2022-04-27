<script lang="ts">
  import { _ } from "svelte-i18n";
  import ClearFilter from "$components/icons/ClearFilter.svelte";
  import ChevronUpIcon from "../icons/ChevronUpIcon.svelte";

  export let title: string;
  export let clearable = false;
  export let initExpanded = false;
  $: rotation = initExpanded
    ? "transition transition-duration-300 rotate-180 mr-1"
    : "transition transition-duration-300 mr-1";
  function toggle() {
    initExpanded = !initExpanded;
    console.log(initExpanded);
  }
</script>

<div
  class="-mx-[0.5em] px-[0.5em] border-[rgba(0, 0, 0, 0.1)] text-lm-dark border border-solid hover:cursor-pointer"
>
  <div
    class="py-2 relative flex justify-between"
    class:text-orange={clearable}
    class:collapsed={!initExpanded}
    data-toggle="collapse"
  >
    <span class="pr-0" on:click={toggle}>
      <ChevronUpIcon {rotation} />
      {$_(title)}</span
    >
    {#if clearable}
      <ClearFilter on:click />
    {/if}
  </div>
  {#if initExpanded}
    <div
      class="shadow-inner bg-lm-light -ml-[0.5em] py-1 pl-2 transition-[all 0.1s ease]"
      class:show={initExpanded}
    >
      <slot />
    </div>
  {/if}
</div>

<style>
  /*<!--  .filter-collapse .toggle .expand-toggle {-->*/
  /*<!--    color: rgba(0, 0, 0, 0.3);-->*/
  /*<!--    font-weight: bold;-->*/
  /*<!--    font-size: 12px;-->*/
  /*<!--    margin-right: 3px;-->*/
  /*<!--    transition: all 0.1s ease;-->*/
  /*<!--  }-->*/

  /*ul {*/
  /*  padding-left: 0.3em;*/
  /*  list-style: none;*/
  /*}*/

  /*.expand-slot {*/
  /*box-shadow: inset 0 3px 7px -3px rgba(0, 0, 0, 0.1),*/
  /*  inset 0 -2px 5px -2px rgba(0, 0, 0, 0.1);*/
  /*background-color: rgba(0, 0, 0, 0.01);*/
  /*padding: 0.5em 0.5em;*/
  /*margin: 0 -0.5em;*/
  /*transition: all 0.1s ease;*/
  /*font-size: 14px;*/
  /*}*/
</style>
