<template>
  <div class="container" style="max-height: 90%; max-width: 100%; padding-top: 0;">
    <div class="row">
      <div class="col" style="min-height: 500px; height: 70vh; padding: 0;">
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
<style lang="scss"></style>
