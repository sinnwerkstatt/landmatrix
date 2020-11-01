<template>
  <div class="datacontainer">
    <ViewSwitcher />
    <FilterBar>
      <h4>{{ $t("Chart") }}</h4>
      <ul class="charts-container-filterbar">
        <li>
          <router-link :to="{ name: 'web-of-transnational-deals' }"
            >Web of Transnational Deals</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'charts' }">Web of Transnational Deals</router-link>
        </li>
      </ul>
    </FilterBar>
    <ChartInformationBar />
    <div class="main-content">
      <LoadingPulse v-if="$apollo.loading" />
      <div class="h-100">
        <div class="sideBuffer float-left"></div>
        <div class="sideBuffer float-right"></div>
        <slot></slot>
      </div>
    </div>
    <!--    {{ this.$store.state.filters.filters }}-->
    <!--    <hr />-->
    <!--    {{ this.$store.getters.filtersForGQL }}-->
  </div>
</template>

<script>
  import LoadingPulse from "/components/Data/LoadingPulse";
  import ViewSwitcher from "/components/Data/ViewSwitcher";
  import FilterBar from "/components/Data/FilterBar";
  import ChartInformationBar from "/components/Data/ChartInformationBar";

  export default {
    name: "Charts",
    components: {
      ChartInformationBar,
      FilterBar,
      ViewSwitcher,
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
    //transition: width 0.5s, min-width 0.5s;

    &.collapsed {
      width: 0;
      min-width: 0;
    }
  }
  .charts-container-filterbar {
    .router-link-exact-active {
      background-color: inherit;
      color: black;
    }
  }
</style>
