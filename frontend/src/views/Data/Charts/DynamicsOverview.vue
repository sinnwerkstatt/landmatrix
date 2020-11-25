<template>
  <ChartsContainer>
    <div class="grid-wrapper">
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
      <div class="grid-container">
        <div class="chart-item left top">
          <h2>Intention of Investment</h2>
<!--          <StatusPieChart-->
<!--            :dealData="implementationStatusData"-->
<!--            :displayLegend="true"-->
<!--            :aspectRatio="aspectRatio"-->
<!--            :maxWidth="'auto'"-->
<!--          ></StatusPieChart>-->
        </div>

        <div class="chart-item right top">
          <h2>Implementation Status</h2>
          <StatusPieChart
            :dealData="implementationStatusData"
            :displayLegend="true"
            :aspectRatio="aspectRatio"
            :maxWidth="'auto'"
          ></StatusPieChart>
        </div>

        <div class="chart-item left bottom">
          <h2>Negotiation Status</h2>
          <StatusPieChart
            :dealData="negotiationStatusData"
            :displayLegend="true"
            :aspectRatio="aspectRatio"
            :maxWidth="'auto'"
          ></StatusPieChart>
        </div>

        <div class="chart-item right bottom">
          <h2>Investment in Agriculture</h2>
<!--          <StatusPieChart-->
<!--            :dealData="negotiationStatusData"-->
<!--            :displayLegend="true"-->
<!--            :aspectRatio="aspectRatio"-->
<!--            :maxWidth="'auto'"-->
<!--          ></StatusPieChart>-->
        </div>
      </div>
    </div>
  </ChartsContainer>
</template>

<script>
  import ChartsContainer from "./ChartsContainer";
  import LoadingPulse from "/components/Data/LoadingPulse";
  import { data_deal_query } from "../query";
  import { prepareNegotianStatusData, sum } from "../../../utils/data_processing";
  import { implementation_status_choices } from "../../../choices";
  import StatusPieChart from "/components/Charts/StatusPieChart";

  export default {
    name: "DynamicsOverview",
    components: { ChartsContainer, LoadingPulse, StatusPieChart },
    apollo: {
      deals: data_deal_query
    },
    data() {
      return {
        deals: [],
        aspectRatio: 1.3,
      };
    },
    computed: {
      intention() {
        return "current_intention_of_investment";
      },
      displayDealsCount: {
        get() {
          return this.$store.state.map.displayDealsCount;
        },
        set(value) {
          this.$store.commit("setDisplayDealsCount", value);
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
      }
    }
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/colors";

  .grid-wrapper {
    padding-top: 3em;
    width: 100%;
    overflow-y: scroll;

    $gutter: 2em;

    .grid-container {
      display: grid;
      padding-bottom: 2em;
      //height: 100%;
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
      }
    }
  }
</style>
