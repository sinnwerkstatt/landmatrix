<template>
  <ChartsContainer>
    <div style="padding: 4em 1em 1em;">
      <h2>Intention of Investment</h2>
      <div class="two-rows" style="width: 600px;">
        <canvas id="intention_deals"></canvas>
        <canvas id="intention_hectares"></canvas>
      </div>
      <!--    <LoadingPulse v-if="$apollo.queries.transnational_deals.loading" />-->
    </div>

    <div style="padding: 4em 1em 1em;">
      <h2>Implementation Status</h2>
      <div class="two-rows" style="width: 600px;">
        <canvas id="implementation_deals"></canvas>
        <canvas id="implementation_hectares"></canvas>
      </div>
      <!--    <LoadingPulse v-if="$apollo.queries.transnational_deals.loading" />-->
    </div>

  </ChartsContainer>
</template>

<script>
  import ChartsContainer from "./ChartsContainer";

  import LoadingPulse from "/components/Data/LoadingPulse";
  import ImplementationStatusChart from "../../../components/Charts/ImplementationStatusChart";
  import { data_deal_query } from "../query";

  export default {
    name: "DynamicsOverview",
    components: { ChartsContainer, LoadingPulse, ImplementationStatusChart },
    apollo: {
      deals: data_deal_query,
    },
    data() {
      return {
        deals: [],
      };
    },
    computed: {
      intention() {
        return "current_intention_of_investment";
      }
    }
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/colors";

  .nav-pills .nav-link.active {
    background: $primary;
  }
</style>
