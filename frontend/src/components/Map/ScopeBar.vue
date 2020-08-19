<template>
  <div class="scope-overlay" :class="{ collapsed: !showScopeOverlay }">
    <div class="toggle-button">
      <a href="#" @click.prevent="showScopeOverlay = !showScopeOverlay">
        <i
          class="fas"
          :class="[showScopeOverlay ? 'fa-chevron-left' : 'fa-chevron-right']"
        ></i>
      </a>
    </div>
    <div class="overlay-content">
      asdf
    </div>
  </div>
</template>

<script>
  export default {
    name: "ScopeBar",
    data() {
      return {
        showScopeOverlay: false,
      };
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";

  .scope-overlay {
    position: absolute;
    background-color: rgba(255, 255, 255, 0.95);
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 10;
    display: flex;
    .toggle-button {
      position: absolute;
      left: 10px;
    }
    .overlay-content {
      width: 20vw;
      max-width: 230px;
      height: 100%;
      overflow-y: auto;
      padding: 0.5em;
    }
    &.collapsed {
      width: 25px;
      .toggle-button {
        position: static;
      }
      .overlay-content {
        display: none;
      }
    }
  }
</style>
