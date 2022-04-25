<script lang="ts">
  import { _ } from "svelte-i18n";
  import ClearFilter from "$components/icons/ClearFilter.svelte";

  export let title: string;
  export let clearable = false;
  export let initExpanded = false;
</script>

<div class="filter-collapse">
  <div
    class="toggle"
    class:text-orange={clearable}
    class:collapsed={!initExpanded}
    data-toggle="collapse"
  >
    <i class="expand-toggle fas fa-chevron-up" />
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
  .filter-collapse {
    margin-left: -0.5em;
    margin-right: -0.5em;
    padding: 5px 0.5em 0 0.5em;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }
  .filter-collapse:hover {
    cursor: pointer;
  }
  .filter-collapse .toggle {
    padding-bottom: 5px;
    position: relative;
  }

  .filter-collapse .toggle .expand-toggle {
    color: rgba(0, 0, 0, 0.3);
    font-weight: bold;
    font-size: 12px;
    margin-right: 3px;
    transition: all 0.1s ease;
  }
  .filter-collapse .toggle.collapsed .expand-toggle {
    transform: rotate(-180deg);
  }

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

  /*.expand-slot .custom-radio {*/
  /*  padding-left: 1.5em;*/
  /*  .custom-control-label {*/
  /*    &:before,*/
  /*    &:after {*/
  /*      width: 1em;*/
  /*      height: 1em;*/
  /*      top: 0.25em;*/
  /*      left: -1.5em;*/
  /*    }*/
  /*    &:after {*/
  /*      top: 0.2em;*/
  /*      width: 0;*/
  /*      height: 0;*/
  /*      left: -1.53em;*/
  /*    }*/
  /*  }*/
  /*}*/
</style>
