<template>
  <ChartsContainer>
    <div class="country-profile">
      <LoadingPulse v-if="$apollo.loading" />
      <IntentionsPerCategory :deals="deals" />
      <LSLAByNegotiation :deals="deals" />
      <DynamicsOfDeal :deals="deals" />
    </div>
  </ChartsContainer>
</template>

<script lang="ts">
  import Vue from "vue";
  import { data_deal_query } from "$views/Data/query";
  import ChartsContainer from "$views/Data/Charts/ChartsContainer.vue";
  import LSLAByNegotiation from "$components/Charts/CountryProfile/LSLAByNegotiation.vue";
  import IntentionsPerCategory from "$components/Charts/CountryProfile/IntentionsPerCategory.vue";
  import DynamicsOfDeal from "$components/Charts/CountryProfile/DynamicsOfDeal.vue";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import type { Deal } from "$types/deal";

  export default Vue.extend({
    name: "CountryProfile",
    components: {
      LoadingPulse,
      DynamicsOfDeal,
      LSLAByNegotiation,
      ChartsContainer,
      IntentionsPerCategory,
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", false));
    },
    data() {
      return { deals: [] as Deal[] };
    },
    metaInfo() {
      return { title: this.$t("Country profile graphs").toString() };
    },
    apollo: { deals: data_deal_query },
  });
</script>
<style lang="scss" scoped>
  .country-profile {
    margin-top: 5rem;
    overflow: visible;
    display: flex;
    flex-direction: column;
    > * {
      flex-shrink: 0;
    }
  }
</style>
