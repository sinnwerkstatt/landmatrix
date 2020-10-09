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
      <p class="mb-1" v-if="currentItem.short_description">{{ currentItem.short_description }}</p>
      <p v-if="currentItem.url">
        <a :href="currentItem.url">Read more</a>
      </p>
      <div v-if="deals.length">
        <div class="toggle-buttons">
          <a href="" @click.prevent="showDealCount=true" :class="{active: showDealCount}">No. of deals</a>
          <a href="" @click.prevent="showDealCount=false" :class="{active: !showDealCount}">Deal size</a>
        </div>
        <div class="total">
          {{ totalCount }}
        </div>
        <div class="chart-wrapper">
          <h5>Negotiation Status</h5>
          <StatusPieChart :dealData="negotiationStatusData" :displayLegend="true"></StatusPieChart>
        </div>
        <div class="chart-wrapper">
          <h5>Implementation Status</h5>
          <StatusPieChart :dealData="implementationStatusData" :displayLegend="true"></StatusPieChart>
        </div>
        <div class="chart-wrapper">
          <h5>Produce</h5>
          <StatusPieChart :dealData="produceData" :legends="produceDataLegendItems"></StatusPieChart>
        </div>
        <div class="get-involved">
          <a href="/newdeal/get-involved/">{{ $t("Contribute") }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StatusPieChart from "../Charts/StatusPieChart";
import gql from "graphql-tag";
import numeral from "numeral/numeral"
import {implementation_status_choices} from "../../choices";

function sum(items, prop) {
  return items.reduce(function (a, b) {
    return a + b[prop];
  }, 0);
};

export default {
  name: "ScopeBar",
  components: {StatusPieChart},
  data() {
    return {
      showDealCount: true,
      deals: [],
      dealsWithExtraInfo: []
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
    dealsWithExtraInfo: {
      query: gql`
        query Deals($limit: Int!, $filters: [Filter]) {
          dealsWithExtraInfo: deals(limit: $limit, filters: $filters) {
            id
            crops
            animals
            resources
          }
        }
      `,
      variables() {
        return {
          limit: 0,
          filters: this.$store.getters.filtersForGQL,
        };
      },
    }
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
            ...country
          }
          if (country.country_page_id) {
            item.url = `/newdeal/country/${country.slug}`
          }
        }
      } else if (this.$store.state.filters.filters.region_id) {
        let region = this.$store.state.page.regions.find(r => r.id === this.$store.state.filters.filters.region_id);
        if (region) {
          item = {
            ...region
          }
          if (region.region_page_id) {
            item.url = `/newdeal/region/${region.slug}`
          }
        }
      }
      return item;
    },
    totalCount() {
      if (this.showDealCount) {
        return numeral(this.deals.length).format("0,0");
      } else {
        return `${numeral(sum(this.deals, 'deal_size')).format('0,0')} ha`;
      }
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
            color: "rgba(252,148,31,0.4)",
          },
          {
            label: "Concluded",
            count: filteredDeals.concluded.length,
            sum: sum(filteredDeals.concluded, 'deal_size'),
            color: "rgba(252,148,31,1)",
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
    },
    implementationStatusData() {
      let data = [];
      if (this.deals.length) {
        let i = 0;
        let colors = ["rgba(252,148,31,0.4)", "rgba(252,148,31,0.7)", "rgba(252,148,31,1)", "#7D4A0F"];
        for (const [key, label] of Object.entries(implementation_status_choices)) {
          let filteredDeals = this.deals.filter(d => {
              return d.current_implementation_status == key
            }
          )
          data.push({
            label: label,
            color: colors[i],
            value: this.showDealCount ? filteredDeals.length : sum(filteredDeals, 'deal_size')
          });
          i++;
        }
      }
      return data;
    },
    produceDataLegendItems() {
      if (this.produceData) {
        return [{
          label: "Crops",
          color: "#FC941F",
        }, {
          label: "Livestock",
          color: "#7D4A0F",
        }, {
          label: "Mineral Resources",
          color: "black",
        }]
      }
    },
    produceData() {
      let data = [];
      let fields = ['crops', 'animals', 'resources']
      let colors = ["#FC941F", "#7D4A0F", "black"]
      if (this.dealsWithExtraInfo.length) {
        let counts = {}
        for (let deal of this.dealsWithExtraInfo) {
          for (let field of fields) {
            counts[field] = counts[field] || [];
            for (let entry of deal[field]) {
              for (let label of entry.value) {
                counts[field][label] = (counts[field][label] + 1) || 1;
              }
            }
          }
        }
        for (let field of fields) {
          for (const [label, count] of Object.entries(counts[field])) {
            if (count > 1) {
              data.push({
                label: label,
                color: colors[fields.indexOf(field)],
                value: count,
              })
            }
          }
        }
        data.sort((a, b) => {
          return b.value - a.value
        })
        let cutOffIndex = Math.min(15, data.length);
        let other = data.slice(cutOffIndex, data.length);
        data = data.slice(0, cutOffIndex);
        for (let d of data) {
          if (d.label in this.produceLabelMap) {
            d.label = this.produceLabelMap[d.label];
          }
        }
        if (other.length) {
          let otherCount = sum(other, 'value');
          data.push({
            label: "Other",
            color: "rgba(252,148,31,0.4)",
            value: otherCount
          });
        }
      }
      return data;
    },
    produceLabelMap() {
      if (this.$store.state.formfields) {
        return {
          ...this.$store.state.formfields.deal.crops.choices,
          ...this.$store.state.formfields.deal.animals.choices,
          ...this.$store.state.formfields.deal.resources.choices,
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
    width: 100%;
    text-align: center;

    h2, p, a {
      text-align: left;
    }


    .toggle-buttons {
      font-size: 0;
      margin-top: 35px;
      margin-bottom: 5px;
      width: 100%;
      text-align: center;

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

    .total {
      width: 100%;
      text-align: center;
      font-weight: bold;
      margin-top: 10px;
      margin-bottom: 10px;
    }

    .chart-wrapper {
      width: 100%;
      margin-bottom: 10px;

      h5 {
        text-align: left;
      }
    }

    .get-involved {
      margin-top: 2em;
      text-align: left;
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
