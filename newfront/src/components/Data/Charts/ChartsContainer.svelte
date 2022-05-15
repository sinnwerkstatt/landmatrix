<script lang="ts">
  import ContextBarContainer from "../ContextBarContainer.svelte";
  import FilterBar from "../FilterBar.svelte";
  import { showContextBar, showFilterBar } from "../index";
</script>

<div class="relative p-0 w-full h-full">
  <!--    <ViewSwitcher />-->
  <FilterBar />
  <ContextBarContainer>
    <slot name="ContextBar" />
  </ContextBarContainer>
  <div class="w-full h-full">
    <div
      class="{$showFilterBar ? 'w-[clamp(220px,20%,300px)]' : 'w-0'} h-full float-left"
    />
    <div
      class="{$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'} h-full float-right"
    />
    <div class="text-center h-full flex justify-center overflow-y-auto overflow-x-auto">
      <slot />
    </div>
  </div>
</div>
