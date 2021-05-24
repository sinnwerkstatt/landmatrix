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

<script>
  import ContextBarWebOfTransnationalDeals from "$components/Charts/ContextBarWebOfTransnationalDeals";
  import LoadingPulse from "$components/Data/LoadingPulse";
  import gql from "graphql-tag";
  import ChartsContainer from "./ChartsContainer";
  import { LandMatrixRadialSpider } from "./d3_hierarchical_edge_bundling";

  export default {
    name: "WebOfTransnationalDeals",
    components: { ChartsContainer, LoadingPulse, ContextBarWebOfTransnationalDeals },
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
      return { title: this.$t("Web of transnational deals") };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.$store.dispatch("showContextBar", true);
      });
    },
    data() {
      return {
        transnational_deals: [],
      };
    },
    computed: {
      filtered_filtersForGQL() {
        return this.$store.getters.filtersForGQL.filter(
          (f) => f.field !== "country_id" && f.field !== "country.fk_region_id"
        );
      },
      filtered_country_id() {
        return this.$store.state.filters.filters.country_id;
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
      redrawSpider() {
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
  };
</script>
<style lang="scss">
  @import "src/scss/colors";

  #svg-container {
    max-height: 100%;
    width: 100%;
    padding: 4em 2em 2em 2em;

    > svg {
      width: 100%;
      height: 100%;

      #incoming-marker {
        fill: $primary;
      }

      #outgoing-marker {
        fill: $lm_investor;
      }

      text {
        font-size: 14px;
        cursor: pointer;

        &.incoming-highlighted {
          font-weight: bold;
          fill: $primary;
        }

        &.outgoing-highlighted {
          font-weight: bold;
          fill: $lm_investor;
        }
      }

      path {
        &.incoming-highlighted {
          stroke: $primary;
          stroke-width: 2;
          marker-start: url(#incoming-marker);
        }

        &.outgoing-highlighted {
          stroke: $lm_investor;
          stroke-width: 2;
          marker-start: url(#outgoing-marker);
        }

        &.incoming-permahighlight {
          stroke: $primary;
          stroke-width: 2.5;
          marker-start: url(#incoming-marker);
        }

        &.outgoing-permahighlight {
          stroke: $lm_investor;
          stroke-width: 2.5;
          marker-start: url(#outgoing-marker);
        }
      }
    }
  }
</style>
