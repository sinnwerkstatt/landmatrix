<template>
  <ul class="legend">
    <li v-for="item in items" :key="item.label" class="legend-item">
      <span class="colored-area" :style="{ backgroundColor: item.color }" />
      <span class="label"> {{ item.label }}</span>
    </li>
  </ul>
</template>

<script lang="ts">
  import Vue from "vue";
  import type { PropType } from "vue";

  interface LegendItem {
    label: string;
    color: string;
  }

  export default Vue.extend({
    props: {
      items: { type: Array as PropType<LegendItem[]>, required: true },
    },
  });
</script>

<style lang="scss" scoped>
  .legend {
    list-style: none;
    padding: 0;
    margin: 1em 3em 0;
    font-size: 0.7rem;
    display: flex;
    justify-content: space-evenly;

    .legend-item {
      .colored-area {
        display: inline-block;
        width: 0.6em;
        height: 0.8em;
        margin-right: 0.2em;
      }
    }
  }
</style>
