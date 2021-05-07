<template>
  <ul class="legend">
    <li v-for="item in items" :key="item.label" class="legend-item">
      <span class="colored-area" :style="getStyle(item)"></span>
      <span class="label">{{ item.label }}</span>
    </li>
  </ul>
</template>

<script>
  export default {
    props: {
      items: { type: Array, required: true },
    },
    methods: {
      getStyle(item) {
        return {
          backgroundColor: item.color,
        };
      },
    },
  };
</script>

<style lang="scss" scoped>
  .legend {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 11px;
    text-align: left;
    .legend-item {
      display: inline-block;
      margin-right: 0.5em;
      &:last-child {
        margin-right: 0;
      }
      .colored-area {
        display: inline-block;
        width: 0.6em;
        height: 0.8em;
      }
      .label {
        margin-left: 0;
      }
    }
  }
</style>
