<template>
  <div class="container">
    <div v-html="mapIntroduction"></div>
    <big-map :options="{ zoom: 2 }" @ready="pinTheMap">
      <template v-slot:overlay>
        <div class="overlay-header" v-if="deals">{{ deals.length }} Deals</div>
        <div class="map-overlay">
          <div v-show="overlayVisible" class="map-overlay-content">
            <div v-show="overlayView === 'deals'" class="tab-content">
              <h4><span>Display</span></h4>
              <div class="js-layer-switch button-layer-switch well">
                <div class="disabled" data-show-layer="countries">
                  <svg
                    version="1.1"
                    id="countries"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    x="0px"
                    y="0px"
                    width="70px"
                    height="70px"
                    viewBox="25 25 50 50"
                    enable-background="new 0 0 100 100"
                    xml:space="preserve"
                  >
                    <circle
                      class="donut-hole"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="#f9de98"
                    ></circle>
                    <circle
                      class="donut-ring"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#d2d3d4"
                      stroke-width="7"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#1D6914"
                      stroke-width="7"
                      stroke-dasharray="69.23076923076923 30.769230769230774"
                      stroke-dashoffset="125"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#2A4BD7"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="55.769230769230774"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#814A19"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="55.769230769230774"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#9DAFFF"
                      stroke-width="7"
                      stroke-dasharray="30.76923076923077 69.23076923076923"
                      stroke-dashoffset="55.769230769230774"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#AD2323"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="25"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#575757"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="25"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#81C57A"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="25"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#8126C0"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="25"
                    ></circle>
                  </svg>
                  <span>Group by country</span>
                </div>
                <div data-show-layer="deals">
                  <svg
                    version="1.1"
                    id="Layer_1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    x="0px"
                    y="0px"
                    width="70px"
                    height="70px"
                    viewBox="25 25 50 50"
                    enable-background="new 0 0 100 100"
                    xml:space="preserve"
                  >
                    <circle
                      class="donut-hole"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="#fff"
                    ></circle>
                    <circle
                      class="donut-ring"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#d2d3d4"
                      stroke-width="7"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#1D6914"
                      stroke-width="7"
                      stroke-dasharray="33.33333333333333 66.66666666666667"
                      stroke-dashoffset="125"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#2A4BD7"
                      stroke-width="7"
                      stroke-dasharray="33.33333333333333 66.66666666666667"
                      stroke-dashoffset="91.66666666666667"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#814A19"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="58.33333333333334"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#9DAFFF"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="58.33333333333334"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#AD2323"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="58.33333333333334"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#575757"
                      stroke-width="7"
                      stroke-dasharray="33.33333333333333 66.66666666666667"
                      stroke-dashoffset="58.33333333333334"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#81C57A"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="25.000000000000014"
                    ></circle>
                    <circle
                      class="donut-segment"
                      cx="50"
                      cy="50"
                      r="15.915494309189533"
                      fill="transparent"
                      stroke="#8126C0"
                      stroke-width="7"
                      stroke-dasharray="0 100"
                      stroke-dashoffset="25.000000000000014"
                    ></circle>
                  </svg>
                  <span>Individual deals</span>
                </div>
              </div>

              <h4><span>Show info about</span></h4>
              <select class="js-legend-select map-legend-select">
                <option value="implementation" selected="selected"
                  >Implementation status
                </option>
                <option value="intention">Intention of investment</option>
                <option value="level_of_accuracy">Spatial accuracy</option>
              </select>
              <h4><span>Areas</span></h4>
              <div class="polygon-legend">
                <label>
                  <input
                    type="checkbox"
                    value="contract_area"
                    name="show-polygons"
                  /><span class="legend-symbol" style="border: 0.15em solid #575757;"
                    ><span
                      class="legend-symbol-inner"
                      style="background-color: #575757; opacity: 0.4;"
                    ></span></span
                  >Contract area
                </label>

                <label>
                  <input
                    type="checkbox"
                    value="intended_area"
                    name="show-polygons"
                  /><span class="legend-symbol" style="border: 0.15em solid #ad2323;"
                    ><span
                      class="legend-symbol-inner"
                      style="background-color: #ad2323; opacity: 0.4;"
                    ></span></span
                  >Intended area
                </label>

                <label>
                  <input
                    type="checkbox"
                    value="production_area"
                    name="show-polygons"
                  /><span class="legend-symbol" style="border: 0.15em solid #1d6914;"
                    ><span
                      class="legend-symbol-inner"
                      style="background-color: #1d6914; opacity: 0.4;"
                    ></span></span
                  >Area in production
                </label>
              </div>
              <h4><span>Legend</span></h4>

              <div class="implementation map-legend active">
                <ul>
                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #1d6914;"
                    ></span
                    >Project not started
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #2a4bd7;"
                    ></span
                    >Startup phase (no production)
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #575757;"
                    ></span
                    >In operation (production)
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #ad2323;"
                    ></span
                    >Project abandoned
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #bab8b8;"
                    ></span
                    >Unknown
                  </li>
                </ul>
              </div>

              <div class="intention map-legend">
                <ul>
                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #1d6914;"
                    ></span
                    >Agriculture
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #2a4bd7;"
                    ></span
                    >Forestry
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #814a19;"
                    ></span
                    >Mining
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #9dafff;"
                    ></span
                    >Tourism
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #ad2323;"
                    ></span
                    >Industry
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #575757;"
                    ></span
                    >Conservation
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #81c57a;"
                    ></span
                    >Renewable Energy
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #8126c0;"
                    ></span
                    >Other
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #bab8b8;"
                    ></span
                    >Unknown
                  </li>
                </ul>
              </div>

              <div class="level_of_accuracy map-legend">
                <ul>
                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #1d6914;"
                    ></span
                    >Country
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #8126c0;"
                    ></span
                    >Administrative region
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #575757;"
                    ></span
                    >Approximate location
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #ad2323;"
                    ></span
                    >Exact location
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #814a19;"
                    ></span
                    >Coordinates
                  </li>

                  <li>
                    <span
                      class="legend-symbol"
                      style="background-color: #bab8b8;"
                    ></span
                    >Unknown
                  </li>
                </ul>
              </div>
            </div>
            <div v-show="overlayView === 'search'" class="tab-content">
              <h4><span>Search</span></h4>
              <p>Type in the field below to search for a location.</p>
              <input
                type="text"
                placeholder="Search location"
                id="map-search-field"
                class="placeholder"
                autocomplete="off"
              />
            </div>
            <div v-show="overlayView === 'context'" class="tab-content">
              <h4><span>Context layers</span></h4>
              <ul class="layer-list">
                <li>
                  <input
                    type="checkbox"
                    id="context-layer-land_cover"
                    name="context-layer"
                    value="land_cover"
                  />
                  <label for="context-layer-land_cover">Land Cover</label>
                  <div class="context-layer-legend"></div>
                </li>
                <li>
                  <input
                    type="checkbox"
                    id="context-layer-cropland"
                    name="context-layer"
                    value="cropland"
                  />
                  <label for="context-layer-cropland">Global Cropland</label>
                  <div class="context-layer-legend"></div>
                </li>
                <li>
                  <input
                    type="checkbox"
                    id="context-layer-ind_oil_palm_concessions"
                    name="context-layer"
                    value="ind_oil_palm_concessions"
                  />
                  <label for="context-layer-ind_oil_palm_concessions"
                    >Oil palm concessions Indonesia</label
                  >
                  <div class="context-layer-legend"></div>
                </li>
              </ul>
            </div>
            <div v-show="overlayView === 'base'" class="tab-content">
              <h4><span>Base layers</span></h4>
              <ul class="layer-list">
                <li>
                  <input type="radio" id="base-layer-osm" checked="checked" />
                  <label for="base-layer-osm">OSM</label>
                </li>
              </ul>
            </div>
            <div v-show="overlayView === 'details'" class="tab-content">
              <div id="details-overlay">
                Please click on a deal or country on the map to select details.
              </div>
            </div>
          </div>
          <div class="map-overlay-tabs">
            <a
              class="list-group-item text-center"
              @click="overlayVisible = !overlayVisible"
            >
              <i
                :class="['lm', overlayVisible ? 'lm-angle-left' : 'lm-angle-right']"
              ></i>
            </a>
            <a
              @click="overlayToggle('deals')"
              class="list-group-item"
              :class="{ active: overlayView === 'deals' }"
            >
              <i class="lm lm-map-marker"></i><br />Deals/Info
            </a>
            <a
              @click="overlayToggle('search')"
              class="list-group-item"
              :class="{ active: overlayView === 'search' }"
            >
              <i class="lm lm-search"></i><br />Search
            </a>
            <a
              @click="overlayToggle('context')"
              class="list-group-item"
              :class="{ active: overlayView === 'context' }"
            >
              <i class="lm lm-map-o"></i><br />Context
            </a>
            <a
              @click="overlayToggle('base')"
              class="list-group-item"
              :class="{ active: overlayView === 'base' }"
            >
              <i class="lm lm-globe"></i><br />Base
            </a>
            <a
              @click="overlayToggle('details')"
              class="list-group-item"
              :class="{ active: overlayView === 'details' }"
            >
              <i class="lm lm-info-circle"></i><br />Details
            </a>
          </div>
        </div>
      </template>
    </big-map>
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";
  import axios from "axios";

  import "leaflet";
  import { PruneCluster, PruneClusterForLeaflet } from "prunecluster-exportable/dist";

  export default {
    name: "GlobalMap",
    components: { BigMap },
    data() {
      return {
        bigmap: null,
        overlayVisible: false,
        overlayView: "deals",
        baseLayers: [],
      };
    },
    computed: {
      mapIntroduction() {
        if (this.$store.state.page.wagtailRootPage)
          return this.$store.state.page.wagtailRootPage.map_introduction;
      },
      deals() {
        return this.$store.state.deal.deals;
      },
    },
    methods: {
      pinTheMap(x) {
        this.bigmap = x;
        if (this.deals) this.addTheMarkers();
        // console.log(this.bigmap);
        var layers = [];
        this.bigmap.eachLayer(function (layer) {
          // console.log(layer._url);
          if (layer instanceof L.TileLayer)
            // console.log(layer._url);
            layers.push(layer);
        });
        // console.log(layers);
      },
      addTheMarkers() {
        // var markers = L.markerClusterGroup();
        // this.locations.map((loc) => {
        //   if(loc.point) {
        //     markers.addLayer(L.marker(loc.point));
        //   }
        // });
        //
        // this.bigmap.addLayer(markers);
        let pruneCluster = new PruneClusterForLeaflet();

        this.deals.map((deal) => {
          deal.locations.map((loc) => {
            if (loc.point) {
              let marker = new PruneCluster.Marker(loc.point.lat, loc.point.lng);
              marker.category = loc.level_of_accuracy;
              pruneCluster.RegisterMarker(marker);
            }
          });
        });

        this.bigmap.addLayer(pruneCluster);
      },
      overlayToggle(name) {
        this.overlayView = name;
        this.overlayVisible = true;
      },
    },
    created() {
      // let query = `query MyLocations($filters: [Filter]) {
      //  locations(limit: 0, filters: $filters) {
      //    id point level_of_accuracy deal { id }
      //  }
      // }`;
      // let variables = {
      //   // filters: [{ field: "deal.deal_size", operation: "GE", value: "200" }],
      // };
      // axios.post("/graphql/", { query, variables }).then((response) => {
      //   this.locations = response.data.data.locations;
      //   if (this.bigmap) this.addTheMarkers();
      // });
    },
    beforeRouteEnter(to, from, next) {
      let title = "Global: Map";
      store.dispatch("setPageContext", {
        title,
        breadcrumbs: [{ link: { name: "wagtail" }, name: "Home" }, { name: title }],
      });
      next();
    },
  };
</script>

<style lang="scss" scoped>
  @import "../scss/colors";

  .overlay-header {
    position: absolute;
    left: 50%;
    top: 0;
    display: flex;
    z-index: 10;
    background: white;
    border-radius: 1px;
    padding: 0 5px;
  }
  .map-overlay {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 10;
    display: flex;
  }

  .map-overlay-content {
    width: 250px;
    height: 75vh;
    min-height: 500px;
    padding-right: 1rem;
    background-color: rgba(255, 255, 255, 0.9);
    float: left;
    overflow-y: auto;
  }

  .map-overlay-tabs {
    float: left;

    .list-group-item {
      padding: 10px 7.5px 5px;
      font-size: 12px;
      position: relative;
      display: block;
      margin-bottom: -1px;
      background-color: rgba(255, 255, 255, 0.9);
      border: 1px solid #ddd;
      border-radius: 0;
      text-align: center !important;

      &.active {
        background: $primary;

        &:hover {
          color: white;
          background: $primary;
          cursor: default;
        }
      }

      &:hover {
        color: #555;
        text-decoration: none;
        background-color: #f5f5f5;
        cursor: pointer;
      }
    }

    i.lm {
      font-size: 25px;
      color: #c6c6c6;
    }
  }
</style>
