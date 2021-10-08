<template>
  <div class="datacontainer">
    <ViewSwitcher />
    <FilterBar @visibility-changed="$emit('filterbar-toggle', $event)" />
    <ContextBarContainer @visibility-changed="$emit('contextbar-toggle', $event)">
      <slot name="ContextBar"></slot>
    </ContextBarContainer>
    <div class="main-content">
      <div class="h-100">
        <div
          :class="{ collapsed: !$store.state.map.showFilterBar }"
          class="sideBuffer float-left"
        ></div>
        <div
          :class="{ collapsed: !$store.state.map.showContextBar }"
          class="sideBuffer float-right"
        ></div>
        <div class="charts-container">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import ContextBarContainer from "$components/Data/ContextBarContainer.vue";
  import FilterBar from "$components/Data/FilterBar.vue";
  import ViewSwitcher from "$components/Data/ViewSwitcher.vue";
  import Vue from "vue";

  export default Vue.extend({
    name: "ChartsContainer",
    components: { ContextBarContainer, FilterBar, ViewSwitcher },
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

  .charts-container {
    text-align: center;
    height: 100%;
    display: flex;
    justify-content: center;
    overflow-y: scroll;
  }

  .sideBuffer {
    min-width: 220px;
    max-width: 300px;
    width: 20%;
    height: 100%;
    min-height: 3px;
    //transition: width 0.5s, min-width 0.5s;

    &.collapsed {
      width: 0;
      min-width: 0;
    }
  }
</style>
