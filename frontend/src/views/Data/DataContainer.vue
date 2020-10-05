<template>
  <div class="datacontainer">
    <ViewSwitcher />
    <FilterBar>
      <slot name="FilterBar"></slot>
    </FilterBar>
    <ScopeBar />
    <div class="main-content">
      <slot></slot>
    </div>
    <!--    {{ this.$store.state.filters.filters }}-->
    <!--    <hr />-->
    <!--    {{ this.$store.getters.filtersForGQL }}-->
  </div>
</template>

<script>
  import FilterBar from "/components/Data/FilterBar";
  import ScopeBar from "/components/Data/ScopeBar";
  import ViewSwitcher from "/components/Data/ViewSwitcher";

  export default {
    name: "DataContainer",
    components: { ScopeBar, FilterBar, ViewSwitcher },
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
