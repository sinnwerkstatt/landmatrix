<script lang="ts">
  import { _ } from "svelte-i18n";
  import BigMap from "$components/Map/BigMap.svelte";
  import { FeatureGroup } from "leaflet";
  import { countries } from "$lib/stores";
  import { getCountryOrRegion } from "$lib/helpers";
  // import { markers_query } from "$store/queries";
  // import { styleCircle } from "./map_helper";
  // import { DivIcon, FeatureGroup, Marker } from "leaflet";
  // import { MarkerClusterGroup } from "leaflet.markercluster/src";

  export let countryID: number;
  export let regionID: number;
  console.log(countryID, regionID);

  const ZOOM_LEVEL_COUNTRY = 4;

  let map = null;
  let featureGroup = new FeatureGroup();
  let markersReady = true;
  let markers = [];

  console.log($countries);
  const roc = regionID
    ? getCountryOrRegion(regionID, true)
    : getCountryOrRegion(countryID);
  console.log(roc);
  //   watch: {
  //     markers() {
  //       this.drawMarkers();
  //     },
  //     roc() {
  //       this.clearMap();
  //       this.focusMap();
  //     },
  //   },
  //   methods: {
  async function bigMapReady(map) {
    // map.addLayer(this.featureGroup);
    this.map = map;
    // this.drawMarkers();
    // this.focusMap();
  }
  //     clearMap() {
  //       this.featureGroup.clearLayers();
  //     },
  //     focusMap() {
  //       if (this.roc) {
  //         if (this.regionId) {
  //           this.map.fitBounds(
  //             [
  //               [this.roc.point_lat_min, this.roc.point_lon_min],
  //               [this.roc.point_lat_max, this.roc.point_lon_max],
  //             ],
  //             { animate: false }
  //           );
  //         } else {
  //           this.map.setView(
  //             [this.roc.point_lat, this.roc.point_lon],
  //             ZOOM_LEVEL_COUNTRY,
  //             { animate: false }
  //           );
  //         }
  //       } else {
  //         this.map.fitWorld({ animate: false });
  //       }
  //     },
  //     _drawGlobalMarkers() {
  //       for (let mark of this.markers) {
  //         let circle = new Marker(mark.coordinates, {
  //           icon: new DivIcon({ className: "landmatrix-custom-circle" }),
  //           regionId: mark.region_id,
  //         });
  //         this.featureGroup.addLayer(circle);
  //
  //         let coun_reg = this.$store.getters.getCountryOrRegion({
  //           type: "region",
  //           id: mark.region_id,
  //         }).name;
  //
  //         styleCircle(circle, mark.count / 50, coun_reg, true, 30);
  //       }
  //     },
  //     _drawRegionMarkers() {
  //       for (let mark of this.markers) {
  //         let circle = new Marker(mark.coordinates, {
  //           icon: new DivIcon({ className: "landmatrix-custom-circle" }),
  //           countryId: mark.country_id,
  //         });
  //         this.featureGroup.addLayer(circle);
  //         styleCircle(circle, mark.count / 20, mark.count, true, 15);
  //       }
  //     },
  //     _drawCountryMarkers() {
  //       // noinspection JSCheckFunctionSignatures
  //       let mcluster = new MarkerClusterGroup({ maxClusterRadius: 20 });
  //       for (let mark of this.markers) {
  //         let circle = new Marker(mark.coordinates);
  //         // this.featureGroup.addLayer(circle);
  //         mcluster.addLayer(circle);
  //       }
  //       this.featureGroup.addLayer(mcluster);
  //     },
  //     drawMarkers() {
  //       if (!this.map || this.markers.length === 0) return;
  //       if (!this.regionId && !this.countryId) this._drawGlobalMarkers();
  //       if (this.regionId) this._drawRegionMarkers();
  //       if (this.countryId) this._drawCountryMarkers();
  //     },
  async function goToGlobalMap() {
    // if (countryID) {
    //   this.$store.dispatch("setFilter", {
    //     filter: "region_id",
    //     value: null,
    //   });
    //   this.$store.dispatch("setFilter", {
    //     filter: "country_id",
    //     value: this.countryId,
    //   });
    // } else {
    //   this.$store.dispatch("setFilter", {
    //     filter: "country_id",
    //     value: null,
    //   });
    //   this.$store.dispatch("setFilter", {
    //     filter: "region_id",
    //     value: this.regionId,
    //   });
    // }
    // this.$router.push({ name: "map" });
  }
</script>

<div
  class="mt-6 w-full min-h-[300px] h-[30vh] relative border border-orange shadow-md rounded cursor-pointer hover:border-orange-300"
  on:click={goToGlobalMap}
>
  <div
    class="group absolute w-full h-full z-[1000] bg-transparent flex hover:bg-orange/20 transition duration-300"
  >
    <span
      class="invisible opacity-0 self-center text-center w-full z-1 text-[4rem] font-bold text-white group-hover:opacity-100  group-hover:visible hover-text transition duration-500"
    >
      {$_("Go to map")}
    </span>
  </div>
  <BigMap
    options={{
      zoomControl: false,
      dragging: false,
      doubleClickZoom: false,
      boxZoom: false,
      center: [12, 30],
    }}
    containerClass="min-h-full h-full"
    hideLayerSwitcher={true}
    on:ready={bigMapReady}
  />
</div>
