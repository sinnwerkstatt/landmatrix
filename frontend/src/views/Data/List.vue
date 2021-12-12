<template>
  <div>
    <DataContainer>
      <template #default>
        <LoadingPulse v-if="$apollo.loading" />
        <div class="h-100">
          <div
            :class="{ collapsed: !$store.state.showFilterBar }"
            class="sideBuffer float-left"
          ></div>
          <div
            :class="{ collapsed: !$store.state.showContextBar }"
            class="sideBuffer float-right"
          ></div>
          <Table :target-model="targetModel"></Table>
        </div>
      </template>
      <template #FilterBar>
        <h4>{{ $t("Data") }}</h4>
        <FilterCollapse :init-expanded="true" :title="$t('Download')">
          <ul>
            <li>
              <a :href="download_link('xlsx')" @click="trackDownload('xlsx')">
                <i class="fas fa-file-download" /> XLSX
              </a>
            </li>
            <li>
              <a :href="download_link('csv')" @click="trackDownload('csv')">
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

<script lang="ts">
  import FilterCollapse from "$components/Data/FilterCollapse.vue";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import Table from "$components/Data/Table.vue";
  import DataContainer from "$components/DataContainer.vue";
  import Vue from "vue";

  export default Vue.extend({
    name: "DataList",
    components: { FilterCollapse, DataContainer, Table, LoadingPulse },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", false));
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
      trackDownload(format) {
        let name = "Global";
        const country_id = this.$store.state.filters.country_id;
        const region_id = this.$store.state.filters.region_id;
        if (country_id) {
          name = this.$store.getters.getCountryOrRegion({
            type: "country",
            id: country_id,
          }).name;
        }
        if (region_id) {
          name = this.$store.getters.getCountryOrRegion({
            type: "region",
            id: region_id,
          }).name;
        }

        window._paq.push(["trackEvent", "Downloads", format, name]);
      },
    },
  });
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
