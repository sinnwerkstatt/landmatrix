<script lang="ts">
  import ContextBarMap from "./ContextBarMap.svelte";
  import FilterBar from "./FilterBar.svelte";
  import ViewSwitcher from "./ViewSwitcher.svelte";
</script>

<div class="relative p-0 w-full h-full">
  <ViewSwitcher />
  <FilterBar>
    <slot name="FilterBar" />
  </FilterBar>
  <ContextBarMap />
  <div class="w-full h-full">
    <slot />
  </div>
</div>
