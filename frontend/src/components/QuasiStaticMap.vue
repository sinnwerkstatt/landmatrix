<template>
  <div class="container">
    <div style="width: 100%; height: 200px; position: relative;">
      <div
        style="position: absolute; width: 100%; height: 100%; z-index: 100000;"
      ></div>
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
  </div>
</template>
<script>
  import BigMap from "./BigMap";
  export default {
    name: "QuasiStaticMap",
    components: { BigMap },
    props: ["country_id", "region_id"],
    methods: {
      bigMapReady(map) {
        let type = 'region'
        let id = this.region_id
        if (this.country_id) {
          type = 'country'
          id = this.country_id
        }
        let roc = this.$store.getters.getCountryOrRegion({ type: type, id:id });
        console.log("x", roc);
        map.fitBounds([
          [roc.point_lat_min, roc.point_lon_min],
          [roc.point_lat_max, roc.point_lon_max],
        ]);
      },
    },
  };
</script>
