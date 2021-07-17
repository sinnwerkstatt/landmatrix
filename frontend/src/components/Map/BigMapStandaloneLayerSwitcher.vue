<template>
  <div class="layerSwitcher" @mouseleave="shown = false">
    <div v-if="!shown" class="layerSwitcherIcon">
      <i class="fas fa-layer-group" @mouseover="shown = true"></i>
    </div>
    <div class="layerSwitcherOptions">
      <ul v-if="shown">
        <li v-for="layer in tileLayers" :key="layer.name">
          <div v-if="layer.name === visibleLayer">{{ layer.name }}</div>
          <a v-else @click.prevent="$store.dispatch('setCurrentLayer', layer.name)">
            {{ layer.name }}
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
  import { mapState } from "vuex";

  export default {
    name: "BigMapStandaloneLayerSwitcher",
    data() {
      return {
        shown: false,
      };
    },
    computed: {
      ...mapState({
        tileLayers: (state) => state.map.layers,
        visibleLayer: (state) => state.map.visibleLayer,
      }),
    },
  };
</script>

<style lang="scss">
  .layerSwitcher {
    position: absolute;
    top: 5px;
    right: 5px;
    z-index: 200;
    padding: 15px 15px 12px;
    background: white;
    color: var(--color-lm-orange);
    border-radius: 5px;

    .layerSwitcherIcon {
      position: absolute;
      top: 0;
      right: 0;

      margin-left: auto;
      margin-right: auto;
      left: 0;
      text-align: center;
    }

    .layerSwitcherOptions {
      ul {
        padding-left: 5px;
        list-style: none;

        div {
          color: black;
        }

        a {
          cursor: pointer;
        }
      }
    }
  }
</style>
