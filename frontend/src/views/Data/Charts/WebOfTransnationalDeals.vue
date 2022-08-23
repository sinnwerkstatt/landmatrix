<template>
  <ChartsContainer>
    <template #default>
      <LoadingPulse v-if="$apollo.queries.transnational_deals.loading" />
      <div id="svg-container">
        <svg></svg>
      </div>
    </template>
    <template #ContextBar>
      <ContextBarWebOfTransnationalDeals :filters="filtered_filtersForGQL" />
    </template>
  </ChartsContainer>
</template>

<script lang="ts">
  import ContextBarWebOfTransnationalDeals from "$components/Charts/ContextBarWebOfTransnationalDeals.vue";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import type { GQLFilter } from "$types/filters";
  import ChartsContainer from "./ChartsContainer.vue";
  import { LandMatrixRadialSpider } from "./d3_hierarchical_edge_bundling";
  import gql from "graphql-tag";
  import Vue from "vue";

  export default Vue.extend({
    name: "WebOfTransnationalDeals",
    components: { ChartsContainer, LoadingPulse, ContextBarWebOfTransnationalDeals },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", true));
    },
    data() {
      return {
        transnational_deals: [],
      };
    },
    apollo: {
      transnational_deals: {
        query: gql`
          query WebOfTransnationalDeals($filters: [Filter]) {
            transnational_deals(filters: $filters)
          }
        `,
        variables() {
          return {
            filters: this.filtered_filtersForGQL,
          };
        },
      },
    },
    metaInfo() {
      return { title: this.$t("Web of transnational deals").toString() };
    },
    computed: {
      filtered_filtersForGQL(): GQLFilter[] {
        return this.$store.getters.filtersForGQL.filter(
          (f) => f.field !== "country_id" && f.field !== "country.region_id"
        );
      },
      filtered_country_id(): number {
        return this.$store.state.filters.country_id;
      },
    },
    watch: {
      transnational_deals() {
        this.redrawSpider();
      },
      filtered_country_id() {
        this.redrawSpider();
      },
    },
    methods: {
      redrawSpider(): void {
        LandMatrixRadialSpider(
          this.transnational_deals,
          "#svg-container > svg",
          this.filtered_country_id,
          (country) => {
            this.$store.dispatch("setFilter", {
              filter: "country_id",
              value: +country,
            });
          }
        );
      },
    },
  });
</script>

<style lang="scss">
  #svg-container {
    max-height: 100%;
    width: 100%;
    padding: 4em 2em 2em 2em;

    > svg {
      width: 100%;
      height: 100%;

      #incoming-marker {
        fill: var(--color-lm-orange);
      }

      #outgoing-marker {
        fill: var(--color-lm-investor);
      }

      text {
        font-size: 14px;
        cursor: pointer;

        &.incoming-highlighted {
          font-weight: bold;
          fill: var(--color-lm-orange);
        }

        &.outgoing-highlighted {
          font-weight: bold;
          fill: var(--color-lm-investor);
        }
      }

      path {
        &.incoming-highlighted {
          stroke: var(--color-lm-orange);
          stroke-width: 2;
          marker-start: url(#incoming-marker);
        }

        &.outgoing-highlighted {
          stroke: var(--color-lm-investor);
          stroke-width: 2;
          marker-start: url(#outgoing-marker);
        }

        &.incoming-permahighlight {
          stroke: var(--color-lm-orange);
          stroke-width: 2.5;
          marker-start: url(#incoming-marker);
        }

        &.outgoing-permahighlight {
          stroke: var(--color-lm-investor);
          stroke-width: 2.5;
          marker-start: url(#outgoing-marker);
        }
      }
    }
  }
</style>
