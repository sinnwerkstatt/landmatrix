<template>
  <div class="static-map" @click="goToGlobalMap">
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
  import BigMap from "./BigMap";

  import { groupBy } from "lodash";

  export default {
    name: "QuasiStaticMap",
    components: { BigMap },
    props: ["country_id", "region_id", "deals"],
    data() {
      return {
        map: null,
        roc: null,
      };
    },
    computed: {
      markers() {
        let markers_list = [];
        for (let deal of this.deals) {
          for (let loc of deal.locations) {
            if (loc.point) {
              let marker = new L.marker([loc.point.lat, loc.point.lng]);
              if (deal.country) {
                marker.country_id = deal.country.id;
              }
              markers_list.push(marker);
            }
          }
        }
        return markers_list;
      },
    },
    methods: {
      bigMapReady(map) {
        map.fitBounds([
          [this.roc.point_lat_min, this.roc.point_lon_min],
          [this.roc.point_lat_max, this.roc.point_lon_max],
        ]);
        this.map = map;
      },
      refreshMap() {
        // group by countries (for region pages)
        Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
          ([key, val]) => {
            let mcluster = L.markerClusterGroup({
              chunkedLoading: true,
            });
            val.forEach((mark) => mcluster.addLayer(mark));
            this.map.addLayer(mcluster);
          }
        );
      },
      goToGlobalMap() {
        if (this.country_id) {
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: this.country_id,
          });
        } else {
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: this.region_id,
          });
        }
        this.$router.push({ name: "map" });
      },
    },
    watch: {
      deals() {
        this.refreshMap();
      },
    },
    created() {
      let type = "region";
      let id = this.region_id;
      if (this.country_id) {
        type = "country";
        id = this.country_id;
      }
      this.roc = this.$store.getters.getCountryOrRegion({ type: type, id: id });
    },
  };
</script>
<style lang="scss">
  @import "../scss/colors";

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
      z-index: 100000;
      background-color: transparent;
      display: flex;

      &:before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background-color: rgba($lm_orange, 0.3);
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
