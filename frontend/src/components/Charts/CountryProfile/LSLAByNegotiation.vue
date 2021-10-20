<template>
  <CountryProfileChartWrapper>
    <h2 slot="heading">LSLAs by negotiation status</h2>
    <div slot="default">
      <div class="sankey-wrapper">
        <LoadingPulse v-if="$apollo.loading" />
        <svg id="lslabyneg"></svg>
      </div>
    </div>
    <!--    <div slot="legend">-->
    <!--      {{ $t("This figure lists the intention of investments per negotiation status.") }}-->
    <!--      <br />-->
    <!--      {{ $t("Please note: a deal may have more than one intention.") }}<br />-->
    <!--      <i v-if="sankey_legend_numbers">-->
    <!--        {{-->
    <!--          $t(-->
    <!--            "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",-->
    <!--            sankey_legend_numbers-->
    <!--          )-->
    <!--        }}-->
    <!--      </i>-->
    <!--    </div>-->
  </CountryProfileChartWrapper>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import CountryProfileChartWrapper from "$components/Charts/CountryProfile/CountryProfileChartWrapper.vue";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import type { Deal } from "$types/deal";
  import { LSLAByNegotiation } from "$components/Charts/CountryProfile/lsla_by_negotiation";

  export default Vue.extend({
    name: "LSLAByNegotiation",
    components: { LoadingPulse, CountryProfileChartWrapper },
    props: {
      deals: { type: [] as PropType<Deal[]>, required: true },
    },
    data() {
      return { svg: null };
    },
    watch: {
      deals() {
        if (!this.deals) return;
        console.log("foo");
      },
    },
    mounted() {
      this.svg = new LSLAByNegotiation("#lslabyneg");
    },
  });
</script>

<style lang="scss" scoped></style>
