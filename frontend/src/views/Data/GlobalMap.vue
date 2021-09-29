<template>
  <div>
    <DataContainer>
      <template #default>
        <LoadingPulse v-if="$apollo.queries.deals.loading" />
        <BigMap
          :center="[12, 30]"
          :container-style="{ height: '100%' }"
          :hide-layer-switcher="true"
          :options="bigmap_options"
          @ready="bigMapIsReady"
        >
        </BigMap>
      </template>
      <template #FilterBar>
        <h4>{{ $t("Map settings") }}</h4>
        <FilterCollapse :init-expanded="true" :title="$t('Displayed data')">
          <b-form-group>
            <b-form-radio
              v-model="displayDealsCount"
              :value="true"
              name="displayDealsCountRadio"
            >
              {{ $t("Number of deal locations") }}
            </b-form-radio>
            <b-form-radio
              v-model="displayDealsCount"
              :value="false"
              name="displayDealsCountRadio"
            >
              {{ $t("Area (ha)") }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse :init-expanded="true" title="Base layer">
          <b-form-group>
            <b-form-radio
              v-for="layer in tileLayers"
              :key="layer.name"
              v-model="visibleLayer"
              :value="layer.name"
              name="layerSelectRadio"
            >
              {{ $t(layer.name) }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse title="Context layers">
          <b-form-group>
            <b-form-checkbox
              v-for="layer in contextLayers"
              :key="layer.name"
              v-model="visibleContextLayers"
              :value="layer"
              name="contextLayerSelect"
            >
              <!-- TODO For some reason some are not shown here... -->
              <!-- {{ $t(layer.name) }}-->
              {{ layer.name }}
              <img
                v-if="visibleContextLayers.includes(layer)"
                :alt="`Legend for ${layer.name}`"
                :src="layer.legendUrlFunction()"
                class="context-layer-legend-image"
              />
            </b-form-checkbox>
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse title="Download">
          <ul>
            <li>
              <a :href="`/api/data.geojson?type=points&filters=${filters}`">
                <i class="fas fa-file-download" /> {{ $t("Locations (as geojson)") }}
              </a>
            </li>
            <li>
              <a :href="`/api/data.geojson?type=areas&filters=${filters}`">
                <i class="fas fa-file-download" /> {{ $t("Areas (as geojson)") }}
              </a>
            </li>
          </ul>
        </FilterCollapse>
      </template>
    </DataContainer>
  </div>
</template>

<script>
  import BigMap from "$components/BigMap";
  import FilterCollapse from "$components/Data/FilterCollapse";
  import LoadingPulse from "$components/Data/LoadingPulse";
  import DataContainer from "$components/DataContainer";
  import MapMarkerPopup from "$components/Map/MapMarkerPopup";
  import { styleCircle } from "$utils/map_helper";

  import { DivIcon, FeatureGroup, LayerGroup, Marker, Popup } from "leaflet";
  import { MarkerClusterGroup } from "leaflet.markercluster/src";
  import { groupBy } from "lodash-es";
  import Vue from "vue";
  import { mapState } from "vuex";
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
    metaInfo() {
      return { title: this.$t("Map") };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", "!isMobile"));
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
        contextLayersLayerGroup: new LayerGroup(),

        markersFeatureGroup: new FeatureGroup(),
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
      filters() {
        return JSON.stringify(this.$store.getters.filtersForGQL);
      },
    },
    apollo: {
      deals: data_deal_query,
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
                let marker = new Marker([loc.point.lat, loc.point.lng]);
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

        new Popup().setContent(popup_content).setLatLng(point).openOn(this.bigmap);
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
        if (!this.bigmap || this.skipMapRefresh) return;

        console.log("Clearing layers");
        this.markersFeatureGroup.clearLayers();
        console.log("Clearing layers: done");

        if (this.deals.length === 0 || this.markers.length === 0) return;

        console.log("Refreshing map");
        this.current_zoom = this.bigmap.getZoom();
        if (this.current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !this.country_id) {
          // cluster by Region
          Object.entries(groupBy(this.markers, (mark) => mark.region_id)).forEach(
            ([key, val]) => {
              if (key === "undefined") return;
              let circle = new Marker(REGION_COORDINATES[key], {
                icon: new DivIcon({ className: "landmatrix-custom-circle" }),
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
              let regname = this.$store.getters.getCountryOrRegion({
                type: "region",
                id: key,
              }).name;
              styleCircle(circle, xval, regname, this.displayDealsCount);
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
              let circle = new Marker(this.country_coords[key], {
                icon: new DivIcon({ className: "landmatrix-custom-circle" }),
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
              let regname = this.$store.getters.getCountryOrRegion({
                type: "country",
                id: key,
              }).name;
              styleCircle(circle, xval, regname, this.displayDealsCount);
            }
          );
        } else {
          // cluster deals with markercluster
          Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
            ([key, val]) => {
              if (key === "undefined") return;
              let mcluster = new MarkerClusterGroup({ chunkedLoading: true });
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
  };
</script>
