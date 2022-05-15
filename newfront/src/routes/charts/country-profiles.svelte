<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { showContextBar } from "$components/Data";

  export const load: Load = async () => {
    showContextBar.set(false);
    return {};
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte";
  import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte";
</script>

<svelte:head>
  <title>{$_("Country profile graphs | Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div
    class="country-profile mt-20 overflow-visible flex flex-col w-[clamp(500px,90%,1000px)]"
  >
    <!--    <LoadingPulse v-if="$apollo.loading" />-->
    <IntentionsPerCategory />
    <LSLAByNegotiation />
    <!--    <DynamicsOfDeal />-->
  </div>
</ChartsContainer>

<!--<style lang="scss" scoped>-->
<!--  .country-profile {-->
<!--    > * {-->
<!--      flex-shrink: 0;-->
<!--    }-->
<!--  }-->
<!--</style>-->
