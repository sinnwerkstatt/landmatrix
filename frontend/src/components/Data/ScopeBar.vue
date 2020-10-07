<template>
  <div class="scope-overlay" :class="{ collapsed: !showScopeOverlay }">
    <span class="wimpel" @click.prevent="showScopeOverlay = !showScopeOverlay">
      <svg viewBox="0 0 2 20" width="20px">
        <path d="M0,0 L2,2 L2,18 L0,20z"></path>
        <text x="0.3" y="11">
          {{ showScopeOverlay ? "&lsaquo;" : "&rsaquo;" }}
        </text>
      </svg>
    </span>
    <div class="overlay-content">
      <h2 v-if="currentItem">{{ currentItem.name }}</h2>
      <p v-if="currentItem.url">
        <a :href="currentItem.url">Read more</a>
      </p>
      <div class="toggle-buttons">
        <a href="" @click.prevent="showDealCount=true" :class="{active: showDealCount}">No. of deals</a>
        <a href="" @click.prevent="showDealCount=false" :class="{active: !showDealCount}">Deal size</a>
      </div>
      <StatusPieChart :title="'Negotiation Status'" :dealData="negotiationStatusData" :showDealCount="showDealCount"></StatusPieChart>
    </div>
  </div>
</template>

<script>
import StatusPieChart from "../Charts/StatusPieChart";
import gql from "graphql-tag";

function sum(items, prop){
  return items.reduce(function (a, b) {
    return a + b[prop];
  }, 0);
};

export default {
  name: "ScopeBar",
  components: {StatusPieChart},
  data() {
    return {
      showScopeOverlay: true,
      showDealCount: true,
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
      showScopeOverlay: {
        get() {
          return this.$store.state.map.showScopeOverlay;
        },
        set(value) {
          this.$store.dispatch("showScopeOverlay", value);
        },
      },
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
    dealFilteredByNegStatus() {
      let filteredDeals = {
        intended: this.deals.filter(
          d => {
            return ['EXPRESSION_OF_INTEREST', 'UNDER_NEGOTIATION', 'MEMORANDUM_OF_UNDERSTANDING'].includes(d.current_negotiation_status)
          }
        ),
        concluded: this.deals.filter(
          d => {
            return ['ORAL_AGREEMENT', 'CONTRACT_SIGNED'].includes(d.current_negotiation_status)
          }
        ),
        failed: this.deals.filter(
          d => {
            return ['NEGOTIATIONS_FAILED', 'CONTRACT_CANCELED'].includes(d.current_negotiation_status)
          }
        )
      }
      if (this.deals.length) {
        return [
          {
            label: "Intended",
            count: filteredDeals.intended.length,
            sum: sum(filteredDeals.intended, 'deal_size'),
            color: "#FDB86A",
          },
          {
            label: "Concluded",
            count: filteredDeals.concluded.length,
            sum: sum(filteredDeals.concluded, 'deal_size'),
            color: "#FC941F",
          },
          {
            label: "Failed",
            count: filteredDeals.failed.length,
            sum: sum(filteredDeals.failed, 'deal_size'),
            color: "#7D4A0F",
          },
        ];
      } else {
        return [];
      }
    },
    negotiationStatusData() {
      if (this.dealFilteredByNegStatus) {
        if (this.showDealCount) {
          return this.dealFilteredByNegStatus.map(d => {
            return {
              value: d.count,
              ...d
            }
          });
        } else {
          return this.dealFilteredByNegStatus.map(d => {
            return {
              value: d.sum,
              ...d
            }
          });
        }
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../scss/colors";

.scope-overlay {
  //border-left: 1px dotted $lm_dark;
  position: absolute;
  background-color: rgba(255, 255, 255, 0.95);
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  display: flex;
  transition: width 0.5s, min-width 0.5s;
  width: 20%;
  min-width: 220px;
  filter: drop-shadow(-3px 3px 3px rgba(0, 0, 0, 0.3));


  .wimpel {
    transform: rotateY(180deg);
    left: -20px;
    right: auto;
  }

  .overlay-content {
    overflow-y: auto;
    padding: 0.7em;

    .toggle-buttons {
      font-size: 0;
      margin-top: 15px;
      margin-bottom: 15px;

      a {
        padding: 0.3em 0.5em;
        background-color: white;
        border: 1px solid $lm_light;
        color: black;
        font-weight: bold;
        font-size: 14px;

        &.active {
          background-color: $primary;
          color: white;
        }
      }
    }
  }

  &.collapsed {
    width: 0;
    min-width: 0;
    .overlay-content {
      display: none;
    }
  }
}
</style>
