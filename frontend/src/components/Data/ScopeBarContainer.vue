<template>
  <div class="scope-bar-container" :class="{ collapsed: !showScopeOverlay }">
    <span class="wimpel" @click.prevent="showScopeOverlay = !showScopeOverlay">
      <svg viewBox="0 0 2 20" width="20px">
        <path d="M0,0 L2,2 L2,18 L0,20z"></path>
        <text x="0.3" y="11">
          {{ showScopeOverlay ? "&lsaquo;" : "&rsaquo;" }}
        </text>
      </svg>
    </span>
    <div class="scope-bar-container-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>

export default {
  name: "ScopeBarContainer",
  data() {
    return {
      showDealCount: true,
      deals: [],
      dealsWithProduceInfo: []
    };
  },
  computed: {
    showScopeOverlay: {
      get() {
        return this.$store.state.map.showScopeOverlay;
      },
      set(value) {
        this.$store.dispatch("showScopeOverlay", value);
      },
    },
  }
};
</script>

<style lang="scss">
@import "../../scss/colors";

.scope-bar-container {
  //border-left: 1px dotted $lm_dark;
  position: absolute;
  background-color: rgba(255, 255, 255, 0.95);
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  display: flex;
  transition: width 0.5s, min-width 0.5s;
  width: 20%;
  min-width: 220px;
  filter: drop-shadow(-3px 3px 3px rgba(0, 0, 0, 0.3));


  .wimpel {
    transform: rotateY(180deg);
    left: -20px;
    right: auto;
  }

  .scope-bar-container-content {
    overflow-y: auto;
    padding: 0.7em;
    width: 100%;
    text-align: center;
  }

  &.collapsed {
    width: 0;
    min-width: 0;

    .scope-bar-container-content {
      display: none;
    }
  }
}
</style>
