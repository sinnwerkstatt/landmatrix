<template>
  <div>
    <DataContainer>
      <template v-slot:default>
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
          <Table :targetModel="targetModel"></Table>
        </div>
      </template>
    </DataContainer>
  </div>
</template>

<script>
  import DataContainer from "./DataContainer";
  import Table from "/components/Data/Table";
  import LoadingPulse from "/components/Data/LoadingPulse";

  export default {
    name: "DataList",
    components: { DataContainer, Table, LoadingPulse },
    computed: {
      targetModel() {
        if (this.$route.name === "list_investors") {
          return "investor";
        } else {
          return "deal";
        }
      },
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.$store.dispatch("showScopeOverlay", false);
      });
    },
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
