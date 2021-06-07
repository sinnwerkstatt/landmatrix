<template>
  <div class="map-container" :style="mapContainerStyle">
    <l-map
      id="bigMap"
      ref="bigMap"
      :options="mapOptions"
      :center="center"
      :bounds="bounds"
      @ready="(map) => $emit('ready', map)"
    >
      <l-tile-layer
        v-for="tileProvider in tileLayers"
        :key="tileProvider.name"
        :name="tileProvider.name"
        :visible="tileProvider.name === visibleLayer"
        :url="tileProvider.url"
        :attribution="tileProvider.attribution"
        :max-zoom="tileProvider.maxZoom || 19"
        layer-type="base"
      />

      <slot />
    </l-map>
    <BigMapStandaloneLayerSwitcher v-if="!hideLayerSwitcher" />
  </div>
</template>

<script>
  import iconRetinaUrl from "$static/images/marker-icon-2x.png";
  import iconUrl from "$static/images/marker-icon.png";
  import shadowUrl from "$static/images/marker-shadow.png";

  import { Icon, Map } from "leaflet";
  import { GestureHandling } from "leaflet-gesture-handling";
  import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css";
  import "leaflet/dist/leaflet.css";
  import { LMap, LTileLayer } from "vue2-leaflet";
  import { mapState } from "vuex";
  import BigMapStandaloneLayerSwitcher from "./Map/BigMapStandaloneLayerSwitcher";

  Map.addInitHook("addHandler", "gestureHandling", GestureHandling);

  delete Icon.Default.prototype._getIconUrl;
  let shadowSize = [0, 0];
  Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl, shadowSize });

  export default {
    name: "BigMap",
    components: {
      BigMapStandaloneLayerSwitcher,
      LMap,
      LTileLayer,
    },
    props: {
      center: { type: Array, default: null },
      options: { type: Object, default: null },
      bounds: { type: Object, default: null },
      containerStyle: { type: Object, default: null },
      hideLayerSwitcher: { type: Boolean, default: false },
    },
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
