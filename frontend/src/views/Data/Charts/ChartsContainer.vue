<template>
  <div class="datacontainer">
    <ViewSwitcher />
    <FilterBar />
    <ContextBarContainer>
      <slot name="ContextBar"></slot>
    </ContextBarContainer>
    <div class="main-content">
      <!--      <LoadingPulse v-if="$apollo.loading" />-->
      <div class="h-100">
        <div
          class="sideBuffer float-left"
          :class="{ collapsed: !$store.state.map.showFilterBar }"
        ></div>
        <div
          class="sideBuffer float-right"
          :class="{ collapsed: !$store.state.map.showContextBar }"
        ></div>
        <div class="charts-container">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ContextBarContainer from "$components/Data/ContextBarContainer";
  import FilterBar from "$components/Data/FilterBar";
  import ViewSwitcher from "$components/Data/ViewSwitcher";

  export default {
    name: "ChartsContainer",
    components: {
      ContextBarContainer,
      FilterBar,
      ViewSwitcher,
    },
    computed: {},
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
