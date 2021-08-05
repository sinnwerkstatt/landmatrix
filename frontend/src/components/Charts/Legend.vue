<template>
  <ul class="legend">
    <li v-for="item in items" :key="item.label" class="legend-item">
      <span class="colored-area" :style="getStyle(item)" />
      <span class="label"> {{ item.label }}</span>
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
