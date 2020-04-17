<template>
  <div class="map-container mt-4">
    <l-map :options="mapOptions" id="globalMap" ref="dealMap">
      <l-control-layers position="topright"></l-control-layers>
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
      <slot></slot>
    </l-map>
  </div>
</template>

<script>

  export default {
    name: "BigMap",
    data() {
      return {
        map_introduction: MAP_INTRODUCTION,
        mapOptions: {
          zoomSnap: 0.5,
          minZoom: 1,
          zoom: 3,
        },
        tileProviders: [
          {
            name: "OpenStreetMap",
            visible: true,
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

  }
</script>

<style lang="scss" scoped>
  #bigMap {
    height: 75vh;
    min-height: 500px;
  }

  .map-container {
    height: 75vh;
    min-height: 500px;
    margin-left: auto;
    margin-right: auto;
    position: relative;

    .overlay {
      position: absolute;
    }
  }

  .leaflet-container {
    background-color: rgba(255, 0, 0, 0);
  }
</style>
