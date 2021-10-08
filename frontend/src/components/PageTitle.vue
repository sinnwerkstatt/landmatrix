<template>
  <div v-if="$slots.default" class="container">
    <h1>
      <span><slot /></span>
    </h1>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";

  export default Vue.extend({
    name: "PageTitle",
    props: {
      title: { type: String, default: "" },
    },
  });
</script>

<style lang="scss" scoped>
  h1 {
    margin-top: 1.25rem;
    font-size: 1.75rem;
    text-align: center;
    color: var(--color-lm-orange);

    &:before {
      background: #c1c1c1;
      content: "";
      display: block;
      height: 1px;
      position: absolute;
      top: 50%;
      width: 100%;
    }
    span {
      font-family: "Unit", sans-serif;
      font-weight: bold;
      text-transform: uppercase;
      background: #ffffff;
      padding: 0 1em;
      position: relative;
      z-index: 1;
    }
  }
</style>
