<template>
  <div class="map-container mt-4" :style="mapContainerStyle">
    <l-map
      :options="mapOptions"
      :center="center || [0, 0]"
      :bounds="bounds"
      id="bigMap"
      ref="bigMap"
      @ready="emitUp"
    >
      <l-control-layers position="bottomright"></l-control-layers>
      <l-control-zoom position="topright"></l-control-zoom>
      <slot name="layers">
        <l-tile-layer
          v-for="tileProvider in tileProviders"
          :key="tileProvider.name"
          :name="tileProvider.name"
          :visible="tileProvider.visible || false"
          :url="tileProvider.url"
          :attribution="tileProvider.attribution"
          :maxZoom="tileProvider.maxZoom || 19"
          layer-type="base"
        />
      </slot>
      <slot></slot>
    </l-map>
    <slot name="overlay"></slot>
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

  const HereApiKey='OgyVd8v9JkEHQIjrK4Q4sEVY-a19xpJXUxWYkTdBQuo';
  export default {
    name: "BigMap",
    components: {
      LMap,
      LTileLayer,
      LControlLayers,
      LGeoJson,
      LControlZoom,
    },
    props: ["center", "options", "bounds", "containerStyle"],
    data() {
      return {
        tileProviders: [
          {
            name: "Here",
            visible: true,
            attribution:
              `Map Tiles &copy; ${new Date().getFullYear()} <a href="http://developer.here.com">HERE</a>`,
            url: `https://2.aerial.maps.ls.hereapi.com/maptile/2.1/maptile/newest/satellite.day/{z}/{x}/{y}/512/png8?apiKey=${HereApiKey}`,
          },
          {
            name: "OpenStreetMap",
            attribution:
              '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          },
          {
            name: "CartoDB Positron",
            url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            attribution:
              '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
          },
          {
            name: "ESRI Satellite",
            url:
              "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attribution:
              "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
          },
          {
            name: "ESRI Topology",
            url:
              "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
            attribution:
              "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community",
          },
          {
            name: "OpenTopoMap",
            maxZoom: 17,
            url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            attribution:
              'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
          },
        ],
      };
    },
    computed: {
      mapOptions() {
        return {
          zoomSnap: 0.5,
          minZoom: 1,
          zoom: 3,
          zoomControl: false,
          ...this.options,
        };
      },
      mapContainerStyle() {
        return {
          "margin-left": "auto",
          "margin-right": "auto",
          position: "relative",
          height: "75vh",
          "min-height": "500px",
          ...this.containerStyle,
        };
      },
    },
    methods: {
      emitUp(x) {
        this.$emit("ready", x);
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
