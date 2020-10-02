<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <ViewSwitcher />
        <FilterBar>
          <slot name="FilterBar"></slot>
        </FilterBar>
        <ScopeBar />
        <slot></slot>
      </div>
    </div>
    <!--    {{ this.$store.state.filters.filters }}-->
    <!--    <hr />-->
    <!--    {{ this.$store.getters.filtersForGQL }}-->
  </div>
</template>

<script>
  import FilterBar from "/components/Map/FilterBar";
  import ScopeBar from "/components/Map/ScopeBar";
  import ViewSwitcher from "/components/Data/ViewSwitcher";

  export default {
    name: "DataContainer",
    components: { ScopeBar, FilterBar, ViewSwitcher },
  };
</script>
<style lang="scss" scoped>
.container {
  max-width: 100%;
  padding-top: 0;
  padding-bottom: 0;
  > .row > .col {
    min-height: 500px;
    height: calc(100vh - 60px - 31px);
    padding: 0;
  }
}
</style>
