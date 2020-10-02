<template>
  <div class="scope-overlay" :class="{ collapsed: !showScopeOverlay }">
    <div class="toggle-button">
      <a href="#" @click.prevent="showScopeOverlay = !showScopeOverlay">
        <i
          class="fas"
          :class="[showScopeOverlay ? 'fa-chevron-left' : 'fa-chevron-right']"
        ></i>
      </a>
    </div>
    <div class="overlay-content">
      <h2 v-if="currentItem">{{ currentItem.name }}</h2>
      <p v-if="currentItem.url">
        <a :href="currentItem.url">Read more</a>
      </p>
      <StatusPieChart :dealData="negotiationStatusData"></StatusPieChart>
    </div>
  </div>
</template>

<script>
import StatusPieChart from "../Charts/StatusPieChart";
import gql from "graphql-tag";

export default {
  name: "ScopeBar",
  components: {StatusPieChart},
  data() {
    return {
      showScopeOverlay: true,
      deals: []
    };
  },
  apollo: {
    deals: {
      query: gql`
        query Deals($limit: Int!, $filters: [Filter]) {
          deals(limit: $limit, filters: $filters) {
            id
            deal_size
            country {
              id
              fk_region {
                id
              }
            }
            # top_investors { id name }
            intention_of_investment
            current_negotiation_status
            current_implementation_status
            locations {
              id
              point
              level_of_accuracy
            }
          }
        }
      `,
      variables() {
        return {
          limit: 0,
          filters: this.$store.getters.filtersForGQL,
        };
      },
    },
  },
  computed: {
    currentItem() {
      let item = {
        name: "Global",
        url: "/newdeal/global"
      };
      if (this.$store.state.filters.filters.country_id) {
        let country = this.$store.state.page.countries.find(c => c.id === this.$store.state.filters.filters.country_id);
        if (country) {
          item = {
            name: country.name,
          }
          if (country.country_page_id) {
            item.url = `/newdeal/country/${country.slug}`
          }
        }
      } else if (this.$store.state.filters.filters.region_id) {
        let region = this.$store.state.page.regions.find(r => r.id === this.$store.state.filters.filters.region_id);
        if (region) {
          item = {
            name: region.name,
          }
          if (region.region_page_id) {
            item.url = `/newdeal/region/${region.slug}`
          }
        }
      }
      return item;
    },
    negotiationStatusData() {
      if (this.deals.length) {
        return [
          {
            label: "Intended",
            count: this.deals.filter(
              d => {
                return ['EXPRESSION_OF_INTEREST', 'UNDER_NEGOTIATION', 'MEMORANDUM_OF_UNDERSTANDING'].includes(d.current_negotiation_status)
              }
            ).length,
            sum: 2357261,
          },
          {
            label: "Concluded",
            count: this.deals.filter(
              d => {
                return ['ORAL_AGREEMENT', 'CONTRACT_SIGNED'].includes(d.current_negotiation_status)
              }
            ).length,
            sum: 3568599,
          },
          {
            label: "Failed",
            count: this.deals.filter(
              d => {
                return ['NEGOTIATIONS_FAILED', 'CONTRACT_CANCELED'].includes(d.current_negotiation_status)
              }
            ).length,
            sum: 35710546,
          },
        ];
      } else {
        return null;
      }
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/colors";

.scope-overlay {
  border-left: 1px dotted $lm_dark;
  position: absolute;
  background-color: rgba(255, 255, 255, 0.95);
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  display: flex;
  transition: width 0.5s;
  width: 20%;

  .toggle-button {
    position: absolute;
    left: -20px;
    transform: rotateY(180deg);
  }

  .overlay-content {
    width: 20vw;
    max-width: 230px;
    height: 100%;
    overflow-y: auto;
    padding: 0.7em;
  }

  &.collapsed {
    width: 0px;

    .overlay-content {
      display: none;
    }
  }
}
</style>
