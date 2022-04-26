<script lang="ts">
  import { _ } from "svelte-i18n";
  import ClearFilter from "$components/icons/ClearFilter.svelte";

  export let title: string;
  export let clearable = false;
  export let initExpanded = false;
</script>

<div
  class="-mx-[0.5em] pt-[5px] px-[0.5em] border-[rgba(0, 0, 0, 0.1)] bordercolor-  border-solid hover:cursor-pointer form-check"
>
  <div
    class="pb-[5px] relative"
    class:text-orange={clearable}
    class:collapsed={!initExpanded}
    data-toggle="collapse"
  >
    <i class="expand-toggle fas fa-chevron-up transform rotate-180" />
    <span class="pr-0">{$_(title)}</span>
    {#if clearable}
      <ClearFilter on:click />
    {/if}
  </div>
  <div class="expand-slot collapse" class:show={initExpanded}>
    <slot />
  </div>
</div>

<style>
  .filter-collapse .toggle .expand-toggle {
    color: rgba(0, 0, 0, 0.3);
    font-weight: bold;
    font-size: 12px;
    margin-right: 3px;
    transition: all 0.1s ease;
  }
  /*.filter-collapse .toggle.collapsed .expand-toggle {*/
  /*  transform: rotate(-180deg);*/
  /*}*/

  ul {
    padding-left: 0.3em;
    list-style: none;
  }

  .expand-slot {
    box-shadow: inset 0 3px 7px -3px rgba(0, 0, 0, 0.1),
      inset 0 -2px 5px -2px rgba(0, 0, 0, 0.1);
    background-color: rgba(0, 0, 0, 0.01);
    padding: 0.5em 0.5em;
    margin: 0 -0.5em;
    transition: all 0.1s ease;
    font-size: 14px;
  }
  .expand-slot > * {
    margin-bottom: 0;
  }
</style>
