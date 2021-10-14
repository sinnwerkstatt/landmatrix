<template>
  <span class="wimpel" :class="{ flipped }" @click.prevent="$emit('click')">
    <svg viewBox="0 0 2 20" width="20px">
      <path d="M0,0 L2,2 L2,18 L0,20z"></path>
      <text x="0.3" y="11">
        {{ showing ? "&lsaquo;" : "&rsaquo;" }}
      </text>
    </svg>
  </span>
</template>

<script lang="ts">
  import Vue from "vue";

  export default Vue.extend({
    name: "Wimpel",
    props: {
      showing: { type: Boolean, default: true },
      flipped: { type: Boolean, default: false },
    },
  });
</script>

<style scoped lang="scss">
  .wimpel {
    position: absolute;
    top: calc(50% - 100px);
    cursor: pointer;
    right: -20px;

    svg {
      opacity: 0.8;
      filter: drop-shadow(1px -1px 1px rgba(0, 0, 0, 0.3));
      color: black;

      path {
        fill: var(--color-lm-orange);
      }

      text {
        font-size: 4px;
        fill: white;
      }
    }
    &.flipped {
      transform: rotateY(180deg);
      left: -20px;
      right: auto;
    }
  }
</style>
