<template>
  <div class="country-profile-chart-wrapper">
    <slot name="heading"></slot>
    <slot name="default"></slot>

    <div class="download-buttons">
      <button class="btn" @click="downloadImage('svg')">
        <i class="fas fa-file-image" /> SVG
      </button>
      <span id="download-png">
        <button
          class="btn"
          :class="{ 'use-chrome': !isChrome }"
          @click="downloadImage('png')"
        >
          <i class="fas fa-file-image" />
          PNG
        </button>
      </span>
      <b-tooltip v-if="!isChrome" target="download-png" triggers="hover">
        At the moment, downloading PNG does not work in Firefox.
      </b-tooltip>
      <span id="download-webp">
        <button
          class="btn"
          :class="{ 'use-chrome': !isChrome }"
          @click="downloadImage('webp')"
        >
          <i class="fas fa-file-image" /> WebP
        </button>
      </span>
      <b-tooltip v-if="!isChrome" target="download-webp" triggers="hover">
        At the moment, downloading WebP does not work in Firefox.
      </b-tooltip>
      <span style="margin: 2rem 0">|</span>
      <button class="btn" @click="downloadJSON">
        <i class="fas fa-file-code" /> JSON
      </button>
      <!--      <button class="btn" @click="downloadCSV">-->
      <!--        <i class="fas fa-file-code" /> CSV-->
      <!--      </button>-->
    </div>
    <div class="legend">
      <slot name="legend" />
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import { data_deal_query_gql } from "$views/Data/query";
  import { a_download, chart_download } from "$utils/charts";
  import type { Deal } from "$types/deal";
  import type { OperationVariables } from "apollo-client/core/types";

  export default Vue.extend({
    name: "CountryProfileChartWrapper",
    components: {},
    data() {
      return { deals: [] as Deal[] };
    },
    apollo: {
      deals: {
        query: data_deal_query_gql,
        variables(): OperationVariables {
          return {
            limit: 0,
            filters: this.$store.getters.filtersForGQL,
            subset: this.$store.getters.userAuthenticated
              ? this.$store.state.filters.publicOnly
                ? "PUBLIC"
                : "ACTIVE"
              : "PUBLIC",
          };
        },
        debounce: 200,
      },
    },
    computed: {
      isChrome(): boolean {
        return /Google Inc/.test(navigator.vendor);
      },
    },
    methods: {
      _fileName(suffix = ""): string {
        let filters = this.$store.state.filters.filters;
        let prefix = "Global - ";
        if (filters.country_id)
          prefix =
            this.$store.getters.getCountryOrRegion({
              type: "country",
              id: filters.country_id,
            }).name + " - ";
        if (filters.region_id)
          prefix =
            this.$store.getters.getCountryOrRegion({
              type: "region",
              id: filters.region_id,
            }).name + " - ";
        return (
          prefix +
          this.$t(
            "Number of intentions per category of production according to implementation status"
          ) +
          suffix
        );
      },
      downloadImage(filetype: string) {
        chart_download(
          document.querySelector("#sankey"),
          `image/${filetype}`,
          this._fileName(`.${filetype}`)
        );
      },
      downloadJSON() {
        let data =
          "data:application/json;charset=utf-8," +
          encodeURIComponent(JSON.stringify(this.sankey_links, null, 2));
        a_download(data, this._fileName(".json"));
      },
      // downloadCSV() {
      //   console.log(this.sankey_links);
      //   let csv = sankey_links_to_csv_cross(this.sankey_links);
      //   let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      //   a_download(data, this._fileName(".csv"));
      //   // this.sankey_links;
      //   // encodeURIComponent();
      // },
    },
  });
</script>

<style lang="scss" scoped>
  .country-profile-chart-wrapper {
    height: 80vh;
    max-height: 80vh;
    margin: 5rem 3rem;
    background: var(--color-lm-orange-light-10);
    border-radius: 1rem;
    padding: 1rem;
    display: flex;
    flex-flow: column wrap;
  }
  .download-buttons {
    background: #2d2d2dff;
    color: var(--color-lm-light);
    border-radius: 0 0 5px 5px;

    button {
      color: var(--color-lm-light);
      font-size: 0.85rem;
      padding: 0 0.75rem 0.15rem;
    }
  }
</style>
