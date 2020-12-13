<template>
  <div class="static-map" @click="goToGlobalMap">
    <LoadingPulse v-if="!markersReady"></LoadingPulse>
    <div class="shield">
      <span class="hover-text">Go to map</span>
    </div>
    <BigMap
      :options="{
        zoomControl: false,
        dragging: false,
        doubleClickZoom: false,
        boxZoom: false,
      }"
      :center="[12, 30]"
      :containerStyle="{ 'min-height': '100%', height: '100%' }"
      :hideLayerSwitcher="true"
      @ready="bigMapReady"
    ></BigMap>
  </div>
</template>
<script>
  import { markers_query } from "../store/queries";
  import { styleCircle } from "../utils/map_helper";
  import BigMap from "./BigMap";
  import LoadingPulse from "./Data/LoadingPulse";

  const ZOOM_LEVEL_COUNTRY = 4;

  export default {
    name: "QuasiStaticMap",
    components: { LoadingPulse, BigMap },
    props: ["country_id", "region_id"],
    data() {
      return {
        map: null,
        featureGroup: L.featureGroup(),
        markersReady: true,
        markers: [],
      };
    },
    apollo: {
      markers: markers_query,
    },
    computed: {
      roc() {
        let type = "region";
        let id = this.region_id;
        if (this.country_id) {
          type = "country";
          id = this.country_id;
        }
        return this.$store.getters.getCountryOrRegion({ type, id });
      },
    },
    methods: {
      bigMapReady(map) {
        map.addLayer(this.featureGroup);
        this.map = map;
        this.focusMap();
      },
      clearMap() {
        this.featureGroup.clearLayers();
      },
      focusMap() {
        if (this.roc) {
          if (this.region_id) {
            this.map.fitBounds(
              [
                [this.roc.point_lat_min, this.roc.point_lon_min],
                [this.roc.point_lat_max, this.roc.point_lon_max],
              ],
              { animate: false }
            );
          } else {
            this.map.setView(
              [this.roc.point_lat, this.roc.point_lon],
              ZOOM_LEVEL_COUNTRY,
              { animate: false }
            );
          }
        } else {
          this.map.fitWorld({ animate: false });
        }
      },
      _drawGlobalMarkers() {
        for (let mark of this.markers) {
          let circle = L.marker(mark.coordinates, {
            icon: L.divIcon({ className: "landmatrix-custom-circle" }),
            region_id: mark.region_id,
          });
          this.featureGroup.addLayer(circle);

          let coun_reg = this.$store.getters.getCountryOrRegion({
            type: "region",
            id: mark.region_id,
          }).name;

          styleCircle(circle, mark.count / 50, coun_reg, true, 3);
        }
      },
      _drawRegionMarkers() {
        for (let mark of this.markers) {
          let circle = L.marker(mark.coordinates, {
            icon: L.divIcon({ className: "landmatrix-custom-circle" }),
            country_id: mark.country_id,
          });
          this.featureGroup.addLayer(circle);
          styleCircle(circle, mark.count / 20, "", true, 5);
        }
      },
      _drawCountryMarkers() {
        // let mcluster = L.markerClusterGroup({ maxClusterRadius: 20 });
        for (let mark of this.markers) {
          let circle = L.marker(mark.coordinates);
          this.featureGroup.addLayer(circle);
          // mcluster.addLayer(circle);
        }
        // this.featureGroup.addLayer(mcluster);
      },
      drawMarkers() {
        if (!this.region_id && !this.country_id) this._drawGlobalMarkers();
        if (this.region_id) this._drawRegionMarkers();
        if (this.country_id) this._drawCountryMarkers();
      },
      goToGlobalMap() {
        if (this.country_id) {
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: null,
          });
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: this.country_id,
          });
        } else {
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: null,
          });
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: this.region_id,
          });
        }
        this.$router.push({ name: "map" });
      },
    },
    watch: {
      markers() {
        this.drawMarkers();
      },
      roc() {
        this.clearMap();
        this.focusMap();
      },
    },
  };
</script>

<style lang="scss">
  @import "src/scss/colors";

  .static-map {
    width: 100%;
    min-height: 300px;
    height: 30vh;
    position: relative;
    border: 1px solid $lm_orange;
    border-radius: 3px;
    box-shadow: 3px 3px 5px rgba(black, 0.3);

    &:hover {
      cursor: pointer;
      box-shadow: 5px 5px 5px rgba(black, 0.3);
      border-color: rgba($lm_orange, 0.7);
    }

    .shield {
      position: absolute;
      width: 100%;
      height: 100%;
      z-index: 1000;
      background-color: transparent;
      display: flex;

      &:before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
      }

      .hover-text {
        display: none;
        color: white;
        font-weight: bold;
        font-size: 4rem;
        align-self: center;
        text-align: center;
        width: 100%;
        z-index: 1;
      }

      &:hover {
        background-color: rgba($lm_orange, 0.5);

        .hover-text {
          display: block;
        }
      }
    }
  }
</style>
