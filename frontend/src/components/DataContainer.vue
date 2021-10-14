<template>
  <div class="datacontainer">
    <ViewSwitcher />
    <FilterBar>
      <slot name="FilterBar"></slot>
    </FilterBar>
    <ContextBarMap />
    <div class="main-content">
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts">
  import ContextBarMap from "$components/Data/ContextBarMap.vue";
  import FilterBar from "$components/Data/FilterBar.vue";
  import ViewSwitcher from "$components/Data/ViewSwitcher.vue";
  import Vue from "vue";

  export default Vue.extend({
    name: "DataContainer",
    components: { ContextBarMap, FilterBar, ViewSwitcher },
  });
</script>
<style lang="scss" scoped>
  .datacontainer {
    position: relative;
    padding: 0;
    width: 100%;
    height: calc(100vh - 60px - 31px);
    .main-content {
      width: 100%;
      height: 100%;
    }
  }
</style>
