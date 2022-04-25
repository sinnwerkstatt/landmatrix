<template>
  <div class="context-bar-container" :class="{ collapsed: !showContextBar }">
    <Wimpel
      :showing="showContextBar"
      :flipped="true"
      @click="showContextBar = !showContextBar"
    />
    <div class="context-bar-container-content">
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts">
  import Wimpel from "$components/Wimpel.vue";
  import Vue from "vue";

  export default Vue.extend({
    name: "ContextBarContainer",
    components: { Wimpel },
    data() {
      return {};
    },
    computed: {
      showContextBar: {
        get() {
          return this.$store.state.showContextBar;
        },
        set(value) {
          this.$store.dispatch("showContextBar", value);
        },
      },
    },
    watch: {
      showContextBar(state) {
        this.$emit("visibility-changed", state);
      },
    },
  });
</script>

<style lang="scss" scoped>
  .context-bar-container {
    //border-left: 1px dotted var(--color-lm-dark);
    position: absolute;
    background-color: rgba(255, 255, 255, 0.95);
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 10;
    display: flex;
    //transition: width 0.5s, min-width 0.5s;
    width: 20%;
    min-width: 220px;
    max-width: 300px;
    filter: drop-shadow(-3px 3px 3px rgba(0, 0, 0, 0.3));

    .context-bar-container-content {
      overflow-y: auto;
      padding: 0.5rem;
      width: 100%;
      text-align: center;

      h2.bar-title {
        font-size: 22px;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        line-height: 1.2;
      }

      h2,
      p,
      a {
        text-align: left;
      }

      p {
        font-size: 0.9rem;
      }
    }

    &.collapsed {
      width: 0;
      min-width: 0;

      .context-bar-container-content {
        display: none;
      }
    }
  }
</style>
