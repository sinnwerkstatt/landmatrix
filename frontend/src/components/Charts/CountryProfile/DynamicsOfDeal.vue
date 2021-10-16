<template>
  <CountryProfileChartWrapper>
    <h2 slot="heading">Dynamics of deal by investor type</h2>

    <div slot="default" class="svg-wrapper">
      <LoadingPulse v-if="$apollo.loading" />
      <svg id="dynamicsofdeal"></svg>
    </div>
    <div slot="legend">
      {{
        $t(
          "Please note: {number} deals have multiple investor types. The full size of the deal is assigned to each investor type.",
          { number: multideals }
        )
      }}<br />
    </div>
  </CountryProfileChartWrapper>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import CountryProfileChartWrapper from "$components/Charts/CountryProfile/CountryProfileChartWrapper.vue";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import type { Deal } from "$types/deal";
  import {
    DynamicsDataPoint,
    DynamicsOfDeal,
  } from "$components/Charts/CountryProfile/dynamics_of_deal";
  import { classification_choices } from "$utils/choices";

  export default Vue.extend({
    name: "DynamicsOfDeal",
    components: { LoadingPulse, CountryProfileChartWrapper },
    props: {
      deals: { type: [] as PropType<Deal[]>, required: true },
    },
    data() {
      return { svg: new DynamicsOfDeal(), multideals: 0 };
    },
    watch: {
      deals() {
        if (!this.svg || !this.deals) return;

        let pots: { [key: string]: number } = {};
        this.deals.forEach((d: Deal) => {
          if (d.top_investors.length > 1) this.multideals += 1;
          d.top_investors.forEach((i) => {
            const cl = i.classification;
            pots[cl] = pots[cl] ? pots[cl] + d.deal_size : d.deal_size;
          });
        });

        const data: DynamicsDataPoint[] = Object.entries(pots).map(([k, v]) => ({
          name: this.$t(classification_choices[k] || "Unknown").toString(),
          value: v,
        }));
        this.svg.do_the_graph("#dynamicsofdeal", data);
      },
    },
  });
</script>

<style lang="scss" scoped>
  .svg-wrapper {
    flex-grow: 1;
    max-width: 100%;
    border-radius: 5px 5px 0 0;
  }
</style>
