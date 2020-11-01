<template>
  <ScopeBarContainer>
    <div class="hint-box">
      <p>
        This interactive graph shows the global flow of transnational land acquisitions.

        <br /><br />
        Country names marked with * have been shortened to improve readability.
      </p>
    </div>
    <div v-if="country" class="hint-box">
      <h4>{{ country.name }}</h4>
      <h5>Regions investing in {{country.name}}</h5>
      DUMMY DATA Asia 6,000 ha (4 deals)<br>
      DUMMY DATA Eastern Europe  6,000 ha (2 deals)<br>
      DUMMY DATA Total 12,000 ha (6 deals)<br>
      Show all inbound deals
      <h5>Regions {{country.name}} invests in</h5>
      DUMMY DATA Eastern Europe 495,000 ha (4 deals)<br>
      DUMMY DATA Total 495,000 ha (4 deals)<br>
      DUMMY DATA Show all outbound deals
    </div>
    <div v-else class="hint-box">
      <h4>World information</h4>
    </div>
  </ScopeBarContainer>
</template>

<script>
  import ScopeBarContainer from "./ScopeBarContainer";
  import { mapState } from "vuex";
  export default {
    name: "ChartInformationBar",
    components: { ScopeBarContainer },
    data() {
      return {};
    },
    computed: {
      ...mapState({
        chartSelectedCountry: (state) => state.chartSelectedCountry,
      }),
      country() {
        if (!this.chartSelectedCountry) return null;
        return this.$store.getters.getCountryOrRegion({
          type: "country",
          id: this.chartSelectedCountry,
        });

      },
    },
  };
</script>

<style lang="scss">
  .hint-box {
    padding: 1em;
    font-size: 0.9em;
    margin-bottom: 20px;
    background-color: #f5f5f5;
    border: 1px solid #e3e3e3;
    border-radius: 4px;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
  }
</style>
