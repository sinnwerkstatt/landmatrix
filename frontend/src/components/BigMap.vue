<template>
  <div class="map-container" :style="mapContainerStyle">
    <l-map
      :options="mapOptions"
      :center="center"
      :bounds="bounds"
      id="bigMap"
      ref="bigMap"
      @ready="emitUp"
    >
      <l-tile-layer
        v-for="tileProvider in tileLayers"
        :key="tileProvider.name"
        :name="tileProvider.name"
        :visible="tileProvider.name === visibleLayer"
        :url="tileProvider.url"
        :attribution="tileProvider.attribution"
        :maxZoom="tileProvider.maxZoom || 19"
        layer-type="base"
      />

      <slot></slot>
    </l-map>
    <BigMapStandaloneLayerSwitcher v-if="!hideLayerSwitcher" />
  </div>
</template>

<script>
  import {
    LControlLayers,
    LControlZoom,
    LGeoJson,
    LMap,
    LTileLayer,
  } from "vue2-leaflet";

  import * as L from "leaflet";
  import { GestureHandling } from "leaflet-gesture-handling";

  import "leaflet/dist/leaflet.css";
  import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css";
  L.Map.addInitHook("addHandler", "gestureHandling", GestureHandling);
  import { Icon } from "leaflet";
  import { mapState } from "vuex";
  import BigMapStandaloneLayerSwitcher from "./Map/BigMapStandaloneLayerSwitcher";

  delete Icon.Default.prototype._getIconUrl;
  Icon.Default.mergeOptions({
    iconRetinaUrl: require("/static/images/marker-icon-2x.png"),
    iconUrl: require("/static/images/marker-icon.png"),
    shadowUrl: require("/static/images/marker-shadow.png"),
  });

  const HereApiKey = "OgyVd8v9JkEHQIjrK4Q4sEVY-a19xpJXUxWYkTdBQuo";
  export default {
    name: "BigMap",
    components: {
      BigMapStandaloneLayerSwitcher,
      LMap,
      LTileLayer,
      LControlLayers,
      LGeoJson,
      LControlZoom,
    },
    props: ["center", "options", "bounds", "containerStyle", "hideLayerSwitcher"],
    computed: {
      ...mapState({
        tileLayers: (state) => state.map.layers,
        visibleLayer: (state) => state.map.visibleLayer,
      }),
      mapOptions() {
        return {
          zoomSnap: 0.5,
          minZoom: 1,
          zoom: 3,
          zoomControl: true,
          gestureHandling: true,
          ...this.options,
        };
      },
      mapContainerStyle() {
        return {
          "margin-left": "auto",
          "margin-right": "auto",
          position: "relative",
          // height: "75vh",
          ...this.containerStyle,
        };
      },
    },
    methods: {
      emitUp(map) {
        this.$emit("ready", map);
      },
    },
  };
</script>

<style lang="scss" scoped>
  .map-container {
    position: relative;

    #bigMap {
      height: 100%;
      z-index: 1;
    }
  }

  .leaflet-container {
    background-color: rgba(255, 0, 0, 0);
  }
</style>
