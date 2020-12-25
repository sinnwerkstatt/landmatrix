<template>
  <div>
    <router-link
      v-if="model === 'deal'"
      class="id-display deal-id-display"
      :to="{ name: 'deal_detail', params: { dealId: value } }"
      >{{ value }}</router-link
    >
    <router-link
      v-else-if="model === 'investor'"
      class="id-display investor-id-display"
      :to="{ name: 'investor_detail', params: { investorId: value } }"
      >{{ value }}</router-link
    >
    <span v-else>{{ value }}</span>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
  };
</script>

<style lang="scss">
  @import "src/scss/colors";

  .id-display {
    display: inline;
    padding: 0.2em 0.6em 0.3em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    color: #fff !important;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: 0.25em;
    &:hover {
      text-decoration: none;
    }
  }
  .investor-id-display {
    background-color: $lm_investor;
    &:hover {
      background-color: darken($lm_investor, 10%);
    }
  }
  .deal-id-display {
    background-color: $lm_orange;
    &:hover {
      background-color: darken($lm_orange, 10%);
    }
  }
</style>
