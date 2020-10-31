<template>
  <ScopeBarContainer>
    <div class="hint-box">
      This interactive graph shows the global flow of transnational land
      acquisitions.<br />
      Clicking on a single country shows its threads in the global pattern: orange lines
      for inbound investments, purple for outbound.
      <br /><br />
      Country names marked with * have been shortened to improve legibility
    </div>
  </ScopeBarContainer>
</template>

<script>
  import ScopeBarContainer from "./ScopeBarContainer";
  export default {
    name: "ChartInformationBar",
    components: { ScopeBarContainer },
    data() {
      return {};
    },
    computed: {},
  };
</script>

<style lang="scss">
  .hint-box {
    padding: 1em;
    margin-bottom: 20px;
    background-color: #f5f5f5;
    border: 1px solid #e3e3e3;
    border-radius: 4px;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
  }
</style>
