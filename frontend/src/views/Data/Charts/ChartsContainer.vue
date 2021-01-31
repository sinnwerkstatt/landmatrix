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
  import ViewSwitcher from "components/Data/ViewSwitcher";
  import FilterBar from "components/Data/FilterBar";
  import ContextBarContainer from "components/Data/ContextBarContainer";

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

<style lang="scss">
  .charts-container {
    text-align: center;
    height: 100%;
    display: flex;
    justify-content: center;
    overflow-y: scroll;
  }
</style>
