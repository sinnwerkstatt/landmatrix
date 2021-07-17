<template>
  <div class="context-bar-container" :class="{ collapsed: !showContextBar }">
    <span class="wimpel" @click.prevent="showContextBar = !showContextBar">
      <svg viewBox="0 0 2 20" width="20px">
        <path d="M0,0 L2,2 L2,18 L0,20z"></path>
        <text x="0.3" y="11">
          {{ showContextBar ? "&lsaquo;" : "&rsaquo;" }}
        </text>
      </svg>
    </span>
    <div class="context-bar-container-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
  export default {
    name: "ContextBarContainer",
    data() {
      return {
        showDealCount: true,
        deals: [],
        dealsWithProduceInfo: [],
      };
    },
    computed: {
      showContextBar: {
        get() {
          return this.$store.state.map.showContextBar;
        },
        set(value) {
          this.$store.dispatch("showContextBar", value);
        },
      },
    },
  };
</script>

<style lang="scss">
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

    .wimpel {
      transform: rotateY(180deg);
      left: -20px;
      right: auto;
    }

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
