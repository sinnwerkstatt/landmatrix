<template>
  <ChartsContainer>
    <template #default>
      <div class="grid-wrapper">
        <div class="grid-container">
          <div class="chart-item left top">
            <h2>{{ $t("Intention of investment") }}</h2>
            <StatusPieChart
              :aspect-ratio="aspectRatio"
              :deal-data="intentionData"
              :legends="intentionLegend"
              :unit="displayDealsCount ? 'deals' : 'ha'"
            ></StatusPieChart>
          </div>

          <div class="chart-item right top">
            <h2>{{ $t("Investment in agriculture") }}</h2>
            <StatusPieChart
              :aspect-ratio="aspectRatio"
              :deal-data="intentionAgricultureData"
              :unit="displayDealsCount ? 'deals' : 'ha'"
            ></StatusPieChart>
          </div>

          <div class="chart-item left bottom">
            <h2>{{ $t("Implementation status") }}</h2>
            <StatusPieChart
              :aspect-ratio="aspectRatio"
              :deal-data="implementationStatusData"
              :unit="displayDealsCount ? 'deals' : 'ha'"
            ></StatusPieChart>
          </div>

          <div class="chart-item right bottom">
            <h2>{{ $t("Negotiation status") }}</h2>
            <StatusPieChart
              :aspect-ratio="aspectRatio"
              :deal-data="negotiationStatusData"
              :unit="displayDealsCount ? 'deals' : 'ha'"
            ></StatusPieChart>
          </div>
        </div>
      </div>
    </template>
    <template #ContextBar>
      <h2 class="bar-title">{{ $t("Dynamics overview charts") }}</h2>
      <div v-html="chart_desc" />
      <DealDisplayToggle />
    </template>
  </ChartsContainer>
</template>

<script lang="ts">
  import { mapState } from "vuex";
  import Vue from "vue";
  import StatusPieChart from "$components/Charts/StatusPieChart.vue";
  import DealDisplayToggle from "$components/Shared/DealDisplayToggle.vue";
  import ChartsContainer from "./ChartsContainer.vue";
  import {
    implementation_status_choices,
    intention_of_investment_choices,
  } from "$utils/choices";
  import { prepareNegotianStatusData, sum } from "$utils/data_processing";
  import { data_deal_query } from "$views/Data/query";

  const NO_INTENTION = "No intention";

  export default Vue.extend({
    name: "DynamicsOverview",
    components: { ChartsContainer, StatusPieChart, DealDisplayToggle },
    metaInfo() {
      return { title: this.$t("Dynamics overview") };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", true));
    },
    apollo: {
      deals: data_deal_query,
    },
    data() {
      return {
        deals: [],
        aspectRatio: 1.3,
      };
    },
    computed: {
      ...mapState({
        displayDealsCount: (state) => state.displayDealsCount,
      }),
      chart_desc(): string {
        if (!this.$store.state.chartDescriptions) return "";
        return this.$store.state.chartDescriptions.dynamics_overview;
      },
      dealsFilteredByNegStatus(): Array<unknown> {
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
      intentionLegend() {
        return [
          { label: "Agriculture", color: "rgba(252,148,31,1)" },
          { label: "Forestry", color: "#7D4A0F" },
          { label: "Other", color: "black" },
          { label: NO_INTENTION, color: "rgba(252,148,31,0.4)" },
        ];
      },
      intentionData() {
        let data = [];
        let colors: string[] = [];
        let otherValue = 0;
        this.intentionLegend.map((l) => {
          colors[l.label] = l.color;
        });
        if (this.deals.length) {
          let groupedDeals = {};
          let totalDeals = 0;
          let totalSize = 0;
          for (let deal of this.deals) {
            if (deal.current_intention_of_investment) {
              for (let int_key of deal.current_intention_of_investment) {
                groupedDeals[int_key] = groupedDeals[int_key] || [];
                groupedDeals[int_key].push(deal);
                totalDeals++;
                totalSize += deal.deal_size;
              }
            } else {
              groupedDeals[NO_INTENTION] = groupedDeals[NO_INTENTION] || [];
              groupedDeals[NO_INTENTION].push(deal);
              totalDeals++;
              totalSize += deal.deal_size;
            }
          }
          for (const [key, keyDeals] of Object.entries(groupedDeals)) {
            let keyGroup = "UNKNOWN";
            let keyLabel = "UNKNOWN";
            if (key === NO_INTENTION) {
              keyGroup = NO_INTENTION;
              keyLabel = NO_INTENTION;
            } else {
              for (const [group, choices] of Object.entries(
                intention_of_investment_choices
              )) {
                if (key in choices) {
                  keyGroup = group;
                  keyLabel = choices[key];
                  break;
                }
              }
            }
            let value = this.displayDealsCount
              ? keyDeals.length
              : sum(keyDeals, "deal_size");

            if (
              (this.displayDealsCount && value < totalDeals * 0.01) ||
              (!this.displayDealsCount && value < totalSize * 0.01)
            ) {
              otherValue += value;
            } else {
              data.push({
                label: keyLabel,
                color: colors[keyGroup],
                group: keyGroup,
                value: value,
                unit: this.displayDealsCount ? "deals" : "ha",
              });
            }
          }
        }
        data.sort((a, b) => {
          return b.value - a.value;
        });
        if (otherValue) {
          data.push({
            label: "Rest",
            color: "rgba(0,0,0,0.1)",
            value: otherValue,
            unit: this.displayDealsCount ? "deals" : "ha",
          });
        }
        return data;
      },
      intentionAgricultureData() {
        return this.intentionData
          .filter((d) => d.group === "Agriculture")
          .map((d, index) => {
            let alphaValue = 1 - index * 0.15;
            return {
              ...d,
              color: "rgba(252,148,31," + alphaValue + ")",
            };
          });
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
              return d.current_implementation_status === key;
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
    },
  });
</script>

<style lang="scss" scoped>
  .grid-wrapper {
    padding-top: 4em;
    padding-bottom: 2em;
    width: 100%;

    $gutter: 2em;

    .grid-container {
      display: grid;

      grid-template-columns: $gutter 1fr $gutter 1fr $gutter;
      grid-template-rows: 1fr $gutter 1fr $gutter;

      .chart-item {
        &.left {
          grid-column: 2 / span 1;
        }

        &.right {
          grid-column: 4 / span 1;
        }

        &.bottom {
          grid-row: 3 / span 1;
        }

        h2 {
          font-size: 1.3rem;
          margin-bottom: 0.7em;
        }
      }
    }
  }
</style>
<style lang="scss">
  .grid-wrapper {
    .chart-item {
      .legend {
        width: 90%;
        margin: 1em auto 0 auto;
        font-size: 0.9rem;
      }
    }
  }
</style>
