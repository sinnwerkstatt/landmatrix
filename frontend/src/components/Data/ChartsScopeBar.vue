<template>
  <ScopeBarContainer>
    <h2 v-if="currentItem">{{ currentItem.name }}</h2>
    <p class="mb-1" v-if="currentItem.short_description">
      {{ currentItem.short_description }}
    </p>
    <p v-if="currentItem.url">
      <a :href="currentItem.url">Read more</a>
    </p>
    <div v-if="deals.length">
      <div class="toggle-buttons">
        <a
          href=""
          @click.prevent="displayDealsCount = true"
          :class="{ active: displayDealsCount }"
        >No. of deals</a
        >
        <a
          href=""
          @click.prevent="displayDealsCount = false"
          :class="{ active: !displayDealsCount }"
        >Deal size</a
        >
      </div>
      <div class="total">
        {{ totalCount }}
      </div>
      <div class="chart-wrapper">
        <h5>Negotiation Status</h5>
        <StatusPieChart
          :dealData="negotiationStatusData"
          :displayLegend="true"
        ></StatusPieChart>
      </div>
      <div class="chart-wrapper">
        <h5>Implementation Status</h5>
        <StatusPieChart
          :dealData="implementationStatusData"
          :displayLegend="true"
        ></StatusPieChart>
      </div>
      <div class="chart-wrapper">
        <h5>Produce</h5>
        <StatusPieChart
          :dealData="produceData"
          :legends="produceDataLegendItems"
        ></StatusPieChart>
      </div>
      <div class="get-involved">
        <router-link :to="`/get-involved/`">{{ $t("Contribute") }}</router-link>
      </div>
    </div>
  </ScopeBarContainer>
</template>

<script>
  import StatusPieChart from "../Charts/StatusPieChart";
  import numeral from "numeral/numeral";
  import { implementation_status_choices } from "../../choices";
  import { prepareNegotianStatusData, sum } from "../../utils/data_processing";
  import { data_deal_produce_query, data_deal_query } from "../../views/Data/query";
  import ScopeBarContainer from "./ScopeBarContainer";

  export default {
    name: "GeneralScopeBar",
    components: { ScopeBarContainer, StatusPieChart },
    data() {
      return {
        deals: [],
        dealsWithProduceInfo: []
      };
    },
    apollo: {
      deals: data_deal_query,
      dealsWithProduceInfo: data_deal_produce_query
    },
    computed: {
      displayDealsCount: {
        get() {
          return this.$store.state.map.displayDealsCount;
        },
        set(value) {
          this.$store.commit("setDisplayDealsCount", value);
        }
      },
      currentItem() {
        let item = {
          name: "Global",
          url: "/newdeal/global"
        };
        if (this.$store.state.filters.filters.country_id) {
          let country = this.$store.state.page.countries.find(
            (c) => c.id === this.$store.state.filters.filters.country_id
          );
          if (country) {
            item = {
              ...country
            };
            if (country.country_page_id) {
              item.url = `/newdeal/country/${country.slug}`;
            }
          }
        } else if (this.$store.state.filters.filters.region_id) {
          let region = this.$store.state.page.regions.find(
            (r) => r.id === this.$store.state.filters.filters.region_id
          );
          if (region) {
            item = {
              ...region
            };
            if (region.region_page_id) {
              item.url = `/newdeal/region/${region.slug}`;
            }
          }
        }
        return item;
      },
      totalCount() {
        if (this.displayDealsCount) {
          return numeral(this.deals.length).format("0,0");
        } else {
          return `${numeral(sum(this.deals, "deal_size")).format("0,0")} ha`;
        }
      },
      dealsFilteredByNegStatus() {
        return prepareNegotianStatusData(this.deals);
      },
      negotiationStatusData() {
        if (this.displayDealsCount) {
          return this.dealsFilteredByNegStatus.map((d) => {
            return { value: d.count, unit: "deals", ...d };
          });
        } else {
          return this.dealsFilteredByNegStatus.map((d) => {
            return { value: d.size, unit: "ha", ...d };
          });
        }
      },
      implementationStatusData() {
        let data = [];
        if (this.deals.length) {
          let i = 0;
          let colors = [
            "rgba(252,148,31,0.4)",
            "rgba(252,148,31,0.7)",
            "rgba(252,148,31,1)",
            "#7D4A0F"
          ];
          for (const [key, label] of Object.entries(implementation_status_choices)) {
            let filteredDeals = this.deals.filter((d) => {
              return d.current_implementation_status == key;
            });
            data.push({
              label: label,
              color: colors[i],
              value: this.displayDealsCount
                ? filteredDeals.length
                : sum(filteredDeals, "deal_size"),
              unit: this.displayDealsCount ? "deals" : "ha"
            });
            i++;
          }
        }
        return data;
      },
      produceDataLegendItems() {
        if (this.produceData) {
          return [
            {
              label: "Crops",
              color: "#FC941F"
            },
            {
              label: "Livestock",
              color: "#7D4A0F"
            },
            {
              label: "Mineral Resources",
              color: "black"
            }
          ];
        }
      },
      produceData() {
        let data = [];
        let fields = ["crops", "animals", "resources"];
        let colors = ["#FC941F", "#7D4A0F", "black"];
        if (this.produceLabelMap && this.dealsWithProduceInfo.length) {
          let counts = {};
          for (let deal of this.dealsWithProduceInfo) {
            for (let field of fields) {
              counts[field] = counts[field] || [];
              for (let entry of deal[field]) {
                for (let label of entry.value) {
                  counts[field][label] = counts[field][label] + 1 || 1;
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
                  value: count
                });
              }
            }
          }
          data.sort((a, b) => {
            return b.value - a.value;
          });
          let totalCount = sum(data, "value");
          let cutOffIndex = Math.min(15, data.length);
          let other = data.slice(cutOffIndex, data.length);
          data = data.slice(0, cutOffIndex);
          for (let d of data) {
            if (d.label in this.produceLabelMap) {
              d.label = this.produceLabelMap[d.label];
            }
            d.value = (d.value / totalCount) * 100;
            d.unit = "%";
            d.precision = 1;
          }
          if (other.length) {
            let otherCount = sum(other, "value");
            data.push({
              label: "Other",
              color: "rgba(252,148,31,0.4)",
              value: (otherCount / totalCount) * 100,
              unit: "%",
              precision: 1
            });
          }
        }
        return data;
      },
      produceLabelMap() {
        if (this.$store.state.formfields && "deal" in this.$store.state.formfields) {
          return {
            ...this.$store.state.formfields.deal.crops.choices,
            ...this.$store.state.formfields.deal.animals.choices,
            ...this.$store.state.formfields.deal.resources.choices
          };
        }
      }
    }
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

  h2,
  p,
  a {
    text-align: left;
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
</style>
<style lang="scss">
  @import "../../scss/colors";

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
</style>
