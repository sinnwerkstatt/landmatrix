<template>
  <div class="datacontainer">
    <ViewSwitcher />
    <FilterBar />
    <ChartInformationBar />
    <div class="main-content">
      <LoadingPulse v-if="$apollo.loading" />
      <div class="h-100">
        <div
          class="sideBuffer float-left"
          :class="{ collapsed: !$store.state.map.showFilterOverlay }"
        ></div>
        <div
          class="sideBuffer float-right"
          :class="{ collapsed: !$store.state.map.showScopeOverlay }"
        ></div>
        <WebOfTransnationalDeals />
      </div>
    </div>
    <!--    {{ this.$store.state.filters.filters }}-->
    <!--    <hr />-->
    <!--    {{ this.$store.getters.filtersForGQL }}-->
  </div>
</template>

<script>
  import LoadingPulse from "/components/Data/LoadingPulse";
  import WebOfTransnationalDeals from "/components/Charts/WebOfTransnationalDeals";
  import ViewSwitcher from "/components/Data/ViewSwitcher";
  import FilterBar from "/components/Data/FilterBar";
  import ChartInformationBar from "/components/Data/ChartInformationBar";

  export default {
    name: "Charts",
    components: {
      ChartInformationBar,
      FilterBar,
      ViewSwitcher,
      WebOfTransnationalDeals,

      LoadingPulse,
    },
    computed: {},
  };
</script>
<style lang="scss">
  .sideBuffer {
    min-width: 230px;
    width: 20%;
    min-height: 3px;
    transition: width 0.5s, min-width 0.5s;

    &.collapsed {
      width: 0;
      min-width: 0;
    }
  }
</style>
