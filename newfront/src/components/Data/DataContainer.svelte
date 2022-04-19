<script lang="ts">
  // import ContextBarMap from "$components/Data/ContextBarMap.vue";
  // import ViewSwitcher from "$components/Data/ViewSwitcher.vue";
  import FilterBar from "./FilterBar.svelte";
</script>

<div class="relative p-0 w-full h-full">
  <!--    <ViewSwitcher />-->
  <FilterBar>
    <slot name="FilterBar" />
  </FilterBar>
  <!--    <ContextBarMap />-->
  <div class="w-full h-full bg-red-200">
    <slot />
  </div>
</div>
