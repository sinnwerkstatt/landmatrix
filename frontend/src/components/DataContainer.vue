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

<script>
  import FilterBar from "$components/Data/FilterBar";
  import ContextBarMap from "$components/Data/ContextBarMap";
  import ViewSwitcher from "$components/Data/ViewSwitcher";

  export default {
    name: "DataContainer",
    components: { ContextBarMap, FilterBar, ViewSwitcher },
  };
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
