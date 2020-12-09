<template>
  <div>
    <DataContainer>
      <template v-slot:default>
        <LoadingPulse v-if="$apollo.queries.deals.loading" />
        <BigMap
          :options="bigmap_options"
          :center="[12, 30]"
          :containerStyle="{ height: '100%' }"
          @ready="bigMapIsReady"
          :hideLayerSwitcher="true"
        >
        </BigMap>
      </template>
      <template v-slot:FilterBar>
        <h4>{{ $t("Map settings") }}</h4>
        <FilterCollapse :title="$t('Displayed data')" :initExpanded="true">
          <b-form-group>
            <b-form-radio
              v-model="displayDealsCount"
              name="displayDealsCountRadio"
              :value="true"
            >
              {{ $t("Number of deal locations") }}
            </b-form-radio>
            <b-form-radio
              v-model="displayDealsCount"
              name="displayDealsCountRadio"
              :value="false"
            >
              {{ $t("Area (ha)") }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse :title="$t('Base layer')" :initExpanded="true">
          <b-form-group>
            <b-form-radio
              v-model="visibleLayer"
              name="layerSelectRadio"
              :value="layer.name"
              v-for="layer in tileLayers"
            >
              {{ layer.name }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse :title="$t('Context layers')">
          <b-form-group>
            <b-form-checkbox
              v-model="visibleContextLayers"
              name="contextLayerSelect"
              :value="layer"
              v-for="layer in contextLayers"
            >
              {{ layer.name }}
              <img
                v-if="visibleContextLayers.includes(layer)"
                :src="layer.legendUrlFunction()"
              />
            </b-form-checkbox>
          </b-form-group>
        </FilterCollapse>
      </template>
    </DataContainer>
  </div>
</template>

<script>
  import "leaflet";
  import "leaflet.markercluster";

  import { primary_color } from "/colors";
  import { groupBy } from "lodash";
  import { mapState } from "vuex";
  import Vue from "vue";

  import MapMarkerPopup from "/components/Map/MapMarkerPopup";
  import DataContainer from "./DataContainer";
  import BigMap from "/components/BigMap";
  import FilterCollapse from "/components/Data/FilterCollapse";
  import LoadingPulse from "/components/Data/LoadingPulse";

  import { data_deal_query } from "./query";

  const ZOOM_LEVEL = {
    REGION_CLUSTERS: 2,
    COUNTRY_CLUSTERS: 3,
    DEAL_CLUSTERS: 5,
    DEAL_PINS: 8,
  };

  const REGION_COORDINATES = {
    2: [6.06433, 17.082249],
    9: [-22.7359, 140.0188],
    21: [54.526, -105.2551],
    142: [34.0479, 100.6197],
    150: [52.0055, 37.9587],
    419: [-4.442, -61.3269],
  };

  export default {
    name: "GlobalMap",
    components: { LoadingPulse, FilterCollapse, DataContainer, BigMap },
    apollo: {
      deals: data_deal_query,
    },
    data() {
      return {
        bigmap: null,
        bigmap_options: {
          minZoom: ZOOM_LEVEL.REGION_CLUSTERS,
          zoom: ZOOM_LEVEL.REGION_CLUSTERS,
          zoomControl: false,
          gestureHandling: false,
        },
        visibleContextLayers: [],
        contextLayersLayerGroup: L.layerGroup(),

        markersFeatureGroup: L.featureGroup(),
        dealLocationMarkersCache: [],
        deals: [],
        markers: [],

        current_zoom: ZOOM_LEVEL.REGION_CLUSTERS,
        skipMapRefresh: false,
      };
    },
    computed: {
      displayDealsCount: {
        get() {
          return this.map.displayDealsCount;
        },
        set(value) {
          this.$store.commit("setDisplayDealsCount", value);
        },
      },
      visibleLayer: {
        get() {
          return this.map.visibleLayer;
        },
        set(value) {
          this.$store.dispatch("setCurrentLayer", value);
        },
      },
      ...mapState({
        // deals: (state) => state.data.deals,
        map: (state) => state.map,
        formfields: (state) => state.formfields,
        tileLayers: (state) => state.map.layers,
        contextLayers: (state) => state.map.contextLayers,
        region_id: (state) => state.filters.filters.region_id,
        country_id: (state) => state.filters.filters.country_id,
        country_coords: (state) => {
          let coords = {};
          state.page.countries.forEach((country) => {
            coords[country.id] = [country.point_lat, country.point_lon];
          });
          return coords;
        },
      }),
    },
    watch: {
      deals() {
        console.log("Watch: deals");
        this.refreshMarkers();
        this.flyToCountryOrRegion();
      },
      bigmap() {
        console.log("Watch: bigmap");
        this.refreshMap();
      },
      current_zoom() {
        console.log("Watch: currentzoom");
        this.refreshMap();
      },
      displayDealsCount() {
        console.log("Watch: displaydealscount");
        this.refreshMap();
      },
      visibleContextLayers(nowlayers, beforelayers) {
        console.log("Watch: visibleContextLayers");
        if (nowlayers.length > beforelayers.length) {
          nowlayers
            .filter((l) => !beforelayers.includes(l))
            .forEach((layer) => this.contextLayersLayerGroup.addLayer(layer.layer));
        }
        if (beforelayers.length > nowlayers.length) {
          beforelayers
            .filter((l) => !nowlayers.includes(l))
            .forEach((layer) => this.contextLayersLayerGroup.removeLayer(layer.layer));
        }
      },
      region_id() {
        console.log("Watch: region_id");
        this.flyToCountryOrRegion();
      },
      country_id() {
        console.log("Watch: country_id");
        this.flyToCountryOrRegion();
      },
    },
    methods: {
      async refreshMarkers() {
        console.log("computing markers ...");
        let markers_list = [];
        for (let deal of this.deals) {
          // console.log("marker", deal.id);
          if (!(deal.id in this.dealLocationMarkersCache)) {
            this.dealLocationMarkersCache[deal.id] = [];
            for (let loc of deal.locations) {
              if (loc.point) {
                let marker = L.marker([loc.point.lat, loc.point.lng], {
                  clickable: true,
                });
                marker.deal = deal;
                marker.loc = loc;
                marker.deal_id = deal.id;
                marker.deal_size = deal.deal_size;
                if (deal.country) {
                  marker.region_id = deal.country.fk_region.id;
                  marker.country_id = deal.country.id;
                }
                marker.on("click", this.createMarkerPopup);

                this.dealLocationMarkersCache[deal.id].push(marker);
              }
            }
          }
          markers_list.push(...this.dealLocationMarkersCache[deal.id]);
        }
        console.log("done");
        this.markers = markers_list;
      },
      createMarkerPopup(event) {
        let marker = event.target;
        let point = this.bigmap.latLngToLayerPoint(marker.getLatLng());
        point = this.bigmap.layerPointToLatLng(point);

        let popup_content = new Vue({
          ...MapMarkerPopup,
          parent: this,
          propsData: { deal: marker.deal, location: marker.loc },
        }).$mount().$el.outerHTML;

        L.popup().setContent(popup_content).setLatLng(point).openOn(this.bigmap);
      },
      styleCircle(circle, size, country_or_region_with_id) {
        let circle_elem = circle.getElement();

        let innertextnode = document.createElement("span");
        innertextnode.className = "landmatrix-custom-circle-text";
        let coun_reg = this.$store.getters.getCountryOrRegion(
          country_or_region_with_id
        );
        if (coun_reg) innertextnode.innerHTML = coun_reg.name;
        circle_elem.append(innertextnode);

        let hoverlabel = document.createElement("span");
        hoverlabel.className = "landmatrix-custom-circle-hover-text";
        circle_elem.append(hoverlabel);

        let factor;
        if (this.displayDealsCount) {
          hoverlabel.innerHTML = `<b>${size}</b> locations`;
          factor = Math.max(Math.log(size) * 17, 40);
        } else {
          hoverlabel.innerHTML = `${size} hectares`;
          factor = Math.max(Math.log(size) * 6, 40);
        }

        Object.assign(circle_elem.style, {
          height: `${factor}px`,
          width: `${factor}px`,
          left: `-${factor / 2}px`,
          top: `-${factor / 2}px`,
          background: primary_color,
        });
      },
      flyToCountryOrRegion() {
        console.log("Should fly now");
        let coords = [0, 0];
        let zoom = ZOOM_LEVEL.REGION_CLUSTERS;
        if (this.country_id) {
          coords = this.country_coords[this.country_id];
          zoom = ZOOM_LEVEL.DEAL_CLUSTERS;
        } else if (this.region_id) {
          coords = REGION_COORDINATES[this.region_id];
          zoom = ZOOM_LEVEL.COUNTRY_CLUSTERS;
        }
        if (zoom < this.current_zoom) {
          // zooming out, apply filter after flying to avoid loading of pins for entire
          // region
          this.skipMapRefresh = true;
          this.bigmap.flyTo(coords, zoom);
          window.setTimeout(() => {
            this.skipMapRefresh = false;
            this.refreshMap();
          }, 1000);
        } else {
          // zooming in, apply filter before flying
          this.refreshMap();
          window.setTimeout(() => {
            this.bigmap.flyTo(coords, zoom);
          }, 700);
        }
      },
      refreshMap() {
        if (
          !this.bigmap ||
          this.deals.length === 0 ||
          this.markers.length === 0 ||
          this.skipMapRefresh
        )
          return;

        console.log("Clearing layers");
        this.markersFeatureGroup.clearLayers();
        console.log("Clearing layers: done");

        console.log("Refreshing map");
        this.current_zoom = this.bigmap.getZoom();
        if (this.current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !this.country_id) {
          // cluster by Region
          Object.entries(groupBy(this.markers, (mark) => mark.region_id)).forEach(
            ([key, val]) => {
              if (key === "undefined") return;
              let circle = L.marker(REGION_COORDINATES[key], {
                icon: L.divIcon({ className: "landmatrix-custom-circle" }),
                region_id: key,
              });
              circle.on("click", (e) => {
                this.$store.dispatch("setFilter", {
                  filter: "region_id",
                  value: +e.target.options.region_id,
                });
              });

              let xval;
              if (this.displayDealsCount) {
                xval = val.length;
              } else {
                xval = val.reduce((x, y) => {
                  return { deal_size: x.deal_size + y.deal_size };
                }).deal_size;
              }

              this.markersFeatureGroup.addLayer(circle);
              this.styleCircle(circle, xval, { type: "region", id: key });
            }
          );
        } else if (
          this.current_zoom < ZOOM_LEVEL.DEAL_CLUSTERS &&
          Object.keys(this.country_coords).length
        ) {
          // cluster by country
          Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
            ([key, val]) => {
              if (key === "undefined") return;
              let circle = L.marker(this.country_coords[key], {
                icon: L.divIcon({ className: "landmatrix-custom-circle" }),
                country_id: key,
              });
              circle.on("click", (e) => {
                this.$store.dispatch("setFilter", {
                  filter: "country_id",
                  value: +e.target.options.country_id,
                });
              });

              let xval;
              if (this.displayDealsCount) {
                xval = val.length;
              } else {
                xval = val.reduce((x, y) => {
                  return { deal_size: x.deal_size + y.deal_size };
                }).deal_size;
              }

              this.markersFeatureGroup.addLayer(circle);
              this.styleCircle(circle, xval, { type: "country", id: key });
            }
          );
        } else {
          // cluster deals with markercluster
          Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
            ([key, val]) => {
              if (key === "undefined") return;
              let mcluster = L.markerClusterGroup({ chunkedLoading: true });
              mcluster.on("clusterclick", (a) => {
                let bounds = a.layer.getBounds().pad(0.5);
                this.bigmap.fitBounds(bounds);
              });
              val.forEach((mark) => {
                mcluster.addLayer(mark);
              });
              this.markersFeatureGroup.addLayer(mcluster);
            }
          );
        }
        console.log("Refreshing map done.");
      },
      bigMapIsReady(bigmap) {
        console.log("The big map is ready.");
        this.bigmap = bigmap;
        this.bigmap.addLayer(this.markersFeatureGroup);
        this.bigmap.addLayer(this.contextLayersLayerGroup);
        bigmap.on("zoomend", () => (this.current_zoom = bigmap.getZoom()));
      },
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        // vm.$store.dispatch("fetchDeals");
        vm.$store.dispatch("showContextBar", true);
      });
    },
  };
</script>

<style lang="scss">
  @import "src/scss/colors";

  .landmatrix-custom-circle {
    opacity: 0.9;
    font-size: 12px;
    line-height: 12px;
    border-radius: 50%;
    border: 0;
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.35));
    display: flex;
    text-align: center;
    justify-content: center;
    align-items: center;

    .landmatrix-custom-circle-hover-text {
      display: none;
      padding: 5px;
    }

    &:hover {
      .landmatrix-custom-circle-text {
        display: none;
      }
      z-index: 900 !important;

      .landmatrix-custom-circle-hover-text {
        display: inline;
      }
    }
  }
  .vue2leaflet-map {
    .marker-cluster-small {
      background-color: rgba(252, 215, 172, 0.5);
      div {
        background-color: rgba(252, 215, 172, 0.8);
      }
    }

    .marker-cluster-medium {
      background-color: rgba(254, 170, 75, 0.5);
      div {
        background-color: rgba(254, 170, 75, 0.8);
      }
    }

    .marker-cluster-large {
      background-color: rgba(252, 148, 31, 0.8);

      div {
        background-color: rgba(252, 148, 31, 0.8);
      }
    }
  }

  .deal-popup {
    .deal-summary {
      color: $lm_dark;
      a {
        color: $lm_investor;
      }
    }
    a.btn-primary {
      margin-top: 1em;
      color: white;
    }
  }
</style>
