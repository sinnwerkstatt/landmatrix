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
      <h2 v-if="currentItem">{{ currentItem.name }}</h2>
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
    computed: {
      currentItem() {
        let item = {
          name: "Global"
        };
        if (this.$store.getters.currentCountryId) {
          let country = this.$store.state.page.countries.find(c => c.id === this.$store.getters.currentCountryId);
          item = {
            name: country.name,
          }
        } else if (this.$store.getters.currentRegionId) {
          let region = this.$store.state.page.regions.find(r => r.id === this.$store.getters.currentRegionId);
          item = {
            name: region.name,
          }
        }
        return item;
      }
    }
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
