<template>
  <ContextBarContainer>
    <div v-if="currentItem">
      <h2 class="bar-title">{{ currentItem.name }}</h2>
      <template v-if="currentItem.observatory">
        <p class="mb-1">
          {{ currentItem.observatory.short_description }}
        </p>
        <p>
          <router-link :to="`/observatory/${currentItem.observatory.meta.slug}/`">
            {{ $t("Read more") }}
          </router-link>
        </p>
      </template>
    </div>
    <div v-if="deals.length">
      <DealDisplayToggle />
      <div class="total">
        {{ totalCount }}
      </div>
      <div class="chart-wrapper">
        <h5>{{ $t("Negotiation status") }}</h5>
        <!--        <p class="hint-box">The negotiation status is filtered at the moment.</p>-->
        <StatusPieChart
          :deal-data="dealsFilteredByNegStatus"
          :display-legend="true"
          :value-field="displayDealsCount ? 'count' : 'size'"
          :unit="displayDealsCount ? 'deals' : 'ha'"
        ></StatusPieChart>
      </div>
      <div class="chart-wrapper">
        <h5>{{ $t("Implementation status") }}</h5>
        <StatusPieChart
          :deal-data="implementationStatusData"
          :display-legend="true"
          value-field="value"
          :unit="displayDealsCount ? 'deals' : 'ha'"
        ></StatusPieChart>
      </div>
      <div class="chart-wrapper">
        <h5>{{ $t("Produce") }}</h5>
        <StatusPieChart
          :deal-data="produceData"
          :legends="produceDataLegendItems"
          unit="%"
        ></StatusPieChart>
      </div>
      <div class="get-involved">
        <router-link :to="`/contribute/`">{{ $t("Contribute") }}</router-link>
      </div>
    </div>
  </ContextBarContainer>
</template>

<script>
  import StatusPieChart from "../Charts/StatusPieChart";
  import numeral from "numeral/numeral";
  import { implementation_status_choices } from "choices";
  import { prepareNegotianStatusData, sum } from "utils/data_processing";
  import { data_deal_produce_query, data_deal_query } from "views/Data/query";
  import ContextBarContainer from "./ContextBarContainer";
  import { mapGetters, mapState } from "vuex";
  import DealDisplayToggle from "../Shared/DealDisplayToggle";

  export default {
    name: "ContextBarMap",
    components: { ContextBarContainer, StatusPieChart, DealDisplayToggle },
    data() {
      return {
        deals: [],
        dealsWithProduceInfo: [],
      };
    },
    apollo: {
      deals: data_deal_query,
      dealsWithProduceInfo: data_deal_produce_query,
    },
    computed: {
      ...mapState({
        displayDealsCount: (state) => state.map.displayDealsCount,
        observatories: (state) => state.page.observatories,
        filters: (state) => state.filters.filters,
      }),
      ...mapGetters(["getCountryOrRegion"]),
      currentItem() {
        let item = null;
        if (this.filters.country_id || this.filters.region_id) {
          if (this.filters.country_id) {
            item = this.getCountryOrRegion({
              id: this.filters.country_id,
            });
          } else {
            item = this.getCountryOrRegion({
              type: "region",
              id: this.filters.region_id,
            });
          }
          if (item.observatory_page_id) {
            item.observatory = this.observatories.filter(
              (o) => o.id === item.observatory_page_id
            )[0];
          }
        } else {
          item = {
            name: "Global",
          };
          item.observatory = this.observatories.filter(
            (o) => !o.country && !o.region
          )[0];
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
            "#7D4A0F",
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
              unit: this.displayDealsCount ? "deals" : "ha",
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
              color: "#FC941F",
            },
            {
              label: "Livestock",
              color: "#7D4A0F",
            },
            {
              label: "Mineral Resources",
              color: "black",
            },
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
              if (deal["current_" + field]) {
                for (let key of deal["current_" + field]) {
                  counts[field][key] = counts[field][key] + 1 || 1;
                }
              }
            }
          }
          for (let field of fields) {
            for (const [key, count] of Object.entries(counts[field])) {
              if (count > 1) {
                data.push({
                  label: key,
                  color: colors[fields.indexOf(field)],
                  value: count,
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
              precision: 1,
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
            ...this.$store.state.formfields.deal.resources.choices,
          };
        }
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

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
      font-size: 18px;
      font-weight: normal;
      margin-top: 1em;
    }
  }

  .get-involved {
    margin-top: 2em;
    text-align: left;
  }
</style>
