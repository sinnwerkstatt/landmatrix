<script lang="ts">
  import ContextBarMap from "./ContextBarMap.svelte";
  import FilterBar from "./FilterBar.svelte";
  import ViewSwitcher from "./ViewSwitcher.svelte";
</script>

<div class="relative h-full w-full p-0">
  <ViewSwitcher />
  <FilterBar>
    <slot name="FilterBar" />
  </FilterBar>
  <ContextBarMap />
  <div class="h-full w-full">
    <slot />
  </div>
</div>
