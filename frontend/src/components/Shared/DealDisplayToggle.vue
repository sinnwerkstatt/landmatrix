<template>
  <div class="toggle-buttons">
    <a
      href=""
      :class="{ active: displayDealsCount }"
      @click.prevent="displayDealsCount = true"
      >No. of deals</a
    >
    <a
      href=""
      :class="{ active: !displayDealsCount }"
      @click.prevent="displayDealsCount = false"
      >Deal size</a
    >
  </div>
</template>

<script>
  export default {
    name: "DealDisplayToggle",
    computed: {
      displayDealsCount: {
        get() {
          return this.$store.state.displayDealsCount;
        },
        set(value) {
          this.$store.commit("setDisplayDealsCount", value);
        },
      },
    },
  };
</script>

<style lang="scss" scoped>
  .toggle-buttons {
    margin-top: 1.5em;
    margin-bottom: 5px;
    width: 100%;
    text-align: center;
    display: flex;
    justify-content: center;

    a {
      padding: 0.3em 0.5em;
      background-color: white;
      border: 1px solid var(--color-lm-light);
      color: black;
      font-weight: bold;
      font-size: 14px;

      &.active {
        background-color: var(--color-lm-orange);
        color: white;
      }
    }
  }
</style>
