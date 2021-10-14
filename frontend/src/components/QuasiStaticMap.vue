<template>
  <div class="static-map" @click="goToGlobalMap">
    <LoadingPulse v-if="!markersReady" />
    <div class="shield">
      <span class="hover-text">{{ $t("Go to map") }}</span>
    </div>
    <BigMap
      :options="{
        zoomControl: false,
        dragging: false,
        doubleClickZoom: false,
        boxZoom: false,
      }"
      :center="[12, 30]"
      :container-style="{ 'min-height': '100%', height: '100%' }"
      :hide-layer-switcher="true"
      @ready="bigMapReady"
    ></BigMap>
  </div>
</template>

<script lang="ts">
  import { markers_query } from "$store/queries";
  import { styleCircle } from "$utils/map_helper";

  import { DivIcon, FeatureGroup, Marker } from "leaflet";
  import { MarkerClusterGroup } from "leaflet.markercluster/src";

  import BigMap from "./BigMap";
  import LoadingPulse from "./Data/LoadingPulse";
  import Vue from "vue";

  const ZOOM_LEVEL_COUNTRY = 4;

  export default Vue.extend({
    name: "QuasiStaticMap",
    components: { LoadingPulse, BigMap },
    props: {
      countryId: { type: Number, required: false, default: null },
      regionId: { type: Number, required: false, default: null },
    },
    data() {
      return {
        map: null,
        featureGroup: new FeatureGroup(),
        markersReady: true,
        markers: [],
      };
    },
    apollo: {
      markers: markers_query,
    },
    computed: {
      roc() {
        if (this.regionId) {
          return this.$store.getters.getCountryOrRegion({
            type: "region",
            id: this.regionId,
          });
        }
        if (this.countryId) {
          return this.$store.getters.getCountryOrRegion({
            type: "country",
            id: this.countryId,
          });
        }
        return null;
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
    methods: {
      bigMapReady(map) {
        map.addLayer(this.featureGroup);
        this.map = map;
        this.drawMarkers();
        this.focusMap();
      },
      clearMap() {
        this.featureGroup.clearLayers();
      },
      focusMap() {
        if (this.roc) {
          if (this.regionId) {
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
          let circle = new Marker(mark.coordinates, {
            icon: new DivIcon({ className: "landmatrix-custom-circle" }),
            regionId: mark.region_id,
          });
          this.featureGroup.addLayer(circle);

          let coun_reg = this.$store.getters.getCountryOrRegion({
            type: "region",
            id: mark.region_id,
          }).name;

          styleCircle(circle, mark.count / 50, coun_reg, true, 30);
        }
      },
      _drawRegionMarkers() {
        for (let mark of this.markers) {
          let circle = new Marker(mark.coordinates, {
            icon: new DivIcon({ className: "landmatrix-custom-circle" }),
            countryId: mark.country_id,
          });
          this.featureGroup.addLayer(circle);
          styleCircle(circle, mark.count / 20, mark.count, true, 15);
        }
      },
      _drawCountryMarkers() {
        // noinspection JSCheckFunctionSignatures
        let mcluster = new MarkerClusterGroup({ maxClusterRadius: 20 });
        for (let mark of this.markers) {
          let circle = new Marker(mark.coordinates);
          // this.featureGroup.addLayer(circle);
          mcluster.addLayer(circle);
        }
        this.featureGroup.addLayer(mcluster);
      },
      drawMarkers() {
        if (!this.map || this.markers.length === 0) return;
        if (!this.regionId && !this.countryId) this._drawGlobalMarkers();
        if (this.regionId) this._drawRegionMarkers();
        if (this.countryId) this._drawCountryMarkers();
      },
      goToGlobalMap() {
        if (this.countryId) {
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: null,
          });
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: this.countryId,
          });
        } else {
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: null,
          });
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: this.regionId,
          });
        }
        this.$router.push({ name: "map" });
      },
    },
  });
</script>

<style lang="scss">
  .static-map {
    margin-top: 1.5em;

    width: 100%;
    min-height: 300px;
    height: 30vh;
    position: relative;
    border: 1px solid var(--color-lm-orange);
    border-radius: 3px;
    box-shadow: 3px 3px 5px rgba(black, 0.3);

    &:hover {
      cursor: pointer;
      box-shadow: 5px 5px 5px rgba(black, 0.3);
      border-color: var(--color-lm-orange-light);
      transition: box-shadow 300ms;
    }

    .shield {
      position: absolute;
      width: 100%;
      height: 100%;
      z-index: 1000;
      background-color: transparent;
      display: flex;
      transition: background-color 600ms;

      &:before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
      }

      .hover-text {
        visibility: hidden;
        opacity: 0;
        transition: 600ms;
        color: white;
        font-weight: bold;
        font-size: 4rem;
        align-self: center;
        text-align: center;
        width: 100%;
        z-index: 1;
      }

      &:hover {
        transition: 300ms;
        background-color: hsla(32, 97%, 55%, 0.2);

        .hover-text {
          transition: 300ms;
          opacity: 1;
          visibility: visible;
        }
      }
    }
  }
</style>
