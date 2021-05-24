<template>
  <div>
    <DataContainer>
      <template #default>
        <LoadingPulse v-if="$apollo.loading" />
        <div class="h-100">
          <div
            class="sideBuffer float-left"
            :class="{ collapsed: !$store.state.map.showFilterBar }"
          ></div>
          <div
            class="sideBuffer float-right"
            :class="{ collapsed: !$store.state.map.showContextBar }"
          ></div>
          <Table :target-model="targetModel"></Table>
        </div>
      </template>
      <template #FilterBar>
        <h4>{{ $t("Data") }}</h4>
        <FilterCollapse title="Download" :init-expanded="true">
          <ul>
            <li>
              <a :href="download_link('xlsx')">
                <i class="fas fa-file-download" /> XLSX
              </a>
            </li>
            <li>
              <a :href="download_link('csv')">
                <i class="fas fa-file-download" /> CSV
              </a>
            </li>
          </ul>
        </FilterCollapse>
        <!--<FilterCollapse :title="$t('Columns')"> </FilterCollapse>-->
      </template>
    </DataContainer>
  </div>
</template>

<script>
  import DataContainer from "$components/DataContainer";
  import Table from "$components/Data/Table";
  import LoadingPulse from "$components/Data/LoadingPulse";
  import FilterCollapse from "$components/Data/FilterCollapse";

  export default {
    name: "DataList",
    components: { FilterCollapse, DataContainer, Table, LoadingPulse },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.$store.dispatch("showContextBar", false);
      });
    },
    metaInfo() {
      return {
        title: this.targetModel === "deal" ? this.$t("Deals") : this.$t("Investors"),
      };
    },
    computed: {
      targetModel() {
        if (this.$route.name === "list_investors") {
          return "investor";
        } else {
          return "deal";
        }
      },
    },
    methods: {
      download_link(format) {
        let filters = JSON.stringify(this.$store.getters.filtersForGQL);
        let subset = this.$store.state.filters.publicOnly ? "PUBLIC" : "ACTIVE";
        return `/api/legacy_export/?filters=${filters}&subset=${subset}&format=${format}`;
      },
    },
  };
</script>
<style lang="scss" scoped>
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
