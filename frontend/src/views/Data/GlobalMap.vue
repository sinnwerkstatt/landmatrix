<template>
  <div>
    <DataContainer>
      <template v-slot:default>
        <LoadingPulse v-if="$apollo.queries.deals.loading" />
        <BigMap
          :options="bigmap_options"
          :center="[12, 30]"
          :containerStyle="{ height: '100%' }"
          @ready="pinTheMap"
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
        <FilterCollapse :title="$t('Base layer')">
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
  import { groupBy } from "lodash";
  import { mapState } from "vuex";
  import { primary_color } from "/colors";

  import BigMap from "/components/BigMap";
  import DataContainer from "./DataContainer";
  import FilterCollapse from "/components/Data/FilterCollapse";
  import LoadingPulse from "/components/Data/LoadingPulse";
  import { data_deal_query } from "./query";
  import { getDealValue } from "../../components/Data/table_mappings";
  import { getFieldValue } from "../../components/Fields/fieldHelpers";

  const ZOOM_LEVEL = {
    REGION_CLUSTERS: 2,
    COUNTRY_CLUSTERS: 3,
    DEAL_CLUSTERS: 5,
    DEAL_PINS: 8,
  };

  export default {
    name: "GlobalMap",
    components: { LoadingPulse, FilterCollapse, DataContainer, BigMap },
    apollo: {
      deals: data_deal_query,
    },
    data() {
      return {
        bigmap_options: {
          minZoom: ZOOM_LEVEL.REGION_CLUSTERS,
          zoom: ZOOM_LEVEL.REGION_CLUSTERS,
          zoomControl: false,
          gestureHandling: false,
        },
        visibleContextLayers: [],
        contextLayersLayerGroup: L.layerGroup(),
        deals: [],
        bigmap: null,
        current_zoom: ZOOM_LEVEL.REGION_CLUSTERS,
        featureGroup: L.featureGroup(),
        region_coords: {
          2: [6.06433, 17.082249],
          9: [-22.7359, 140.0188],
          21: [54.526, -105.2551],
          142: [34.0479, 100.6197],
          150: [52.0055, 37.9587],
          419: [-4.442, -61.3269],
        },
        skipMapRefresh: false,
        dealLocationMarkersCache: [],
      };
    },
    computed: {
      displayDealsCount: {
        get() {
          return this.$store.state.map.displayDealsCount;
        },
        set(value) {
          this.$store.commit("setDisplayDealsCount", value);
        },
      },
      visibleLayer: {
        get() {
          return this.$store.state.map.visibleLayer;
        },
        set(value) {
          this.$store.dispatch("setCurrentLayer", value);
        },
      },
      ...mapState({
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
        markers() {
          console.log("computing markers ...")
          let markers_list = [];
          for (let deal of this.deals) {
            if (!(deal.id in this.dealLocationMarkersCache)) {
              this.dealLocationMarkersCache[deal.id] = [];
              for (let loc of deal.locations) {
                if (loc.point) {
                  let marker = new L.marker([loc.point.lat, loc.point.lng]);
                  marker.deal_id = deal.id;
                  marker.deal_size = deal.deal_size;
                  if (deal.country) {
                    marker.region_id = deal.country.fk_region.id;
                    marker.country_id = deal.country.id;
                  }
                  var popupStatic = '<div style="height:100px; width:100px"></div>';
                  marker.bindPopup(popupStatic);
                  marker.on('click', (e) => {
                    let popup = e.target.getPopup();
                    popup.setContent(this.getPopupHtml(deal, loc));
                  });
                  this.dealLocationMarkersCache[deal.id].push(marker);
                }
              }
            }
            markers_list.push(...this.dealLocationMarkersCache[deal.id])
          }
          console.log("done")
          return markers_list;
        },
      }),
    },
    watch: {
      deals() {
        console.log("Watch: deals")
        this.flyToCountryOrRegion();
      },
      // markers() {
      //   console.log("Watch: markers")
      //   this.refreshMap();
      // },
      // bigmap() {
      //   console.log("Watch: bigmap")
      //   this.refreshMap();
      // },
      current_zoom() {
        console.log("Watch: currentzoom")
        this.refreshMap();
      },
      "$store.state.map.displayDealsCount": function () {
        console.log("Watch: displaydealscount")
        this.refreshMap();
      },
      visibleContextLayers() {
        console.log("Watch: visibleContextLayers")
        this.contextLayersLayerGroup.clearLayers();
        this.visibleContextLayers.forEach((layer) => {
          let ctxlayer = L.tileLayer.wms(layer.url, layer.params);
          ctxlayer.setOpacity(0.7);
          this.contextLayersLayerGroup.addLayer(ctxlayer);
          if (layer.legendUrlFunction) {
            console.log(layer.legendUrlFunction());
          }
        });
      },
      "$store.state.page.regions": function () {
        console.log("Watch: regions")
        // otherwise country name will not be displayed on initial load with small list of
        // filtered deals (e.g. single country)
        // TODO: Make sure that countries/regions are loaded before deals?!
        this.refreshMap();
        this.flyToCountryOrRegion();
      },
      region_id() {
        console.log("Watch: region_id")
        this.flyToCountryOrRegion();
      },
      country_id() {
        console.log("Watch: country_id")
        this.flyToCountryOrRegion();
      },
    },
    methods: {
      flyToCountryOrRegion() {
        console.log("Should fly now")
        let coords = [0, 0];
        let zoom = ZOOM_LEVEL.REGION_CLUSTERS;
        if (this.country_id) {
          coords = this.country_coords[this.country_id];
          zoom = ZOOM_LEVEL.DEAL_CLUSTERS;
        } else if (this.region_id) {
          coords = this.region_coords[this.region_id];
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
          factor = Math.max(Math.log(size) * 16, 40);
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
      refreshMap() {
        console.log("Should refresh map now")
        if (this.skipMapRefresh) return;
        console.log("Clearing layers")
        this.featureGroup.clearLayers();
        console.log("Clearing layers: done")
        if (this.bigmap && this.markers.length > 0) {
          console.log("Refreshing map")
          this.current_zoom = this.bigmap.getZoom();
          if (this.current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !this.country_id) {
            // cluster by Region
            Object.entries(groupBy(this.markers, (mark) => mark.region_id)).forEach(
              ([key, val]) => {
                let circle = L.marker(this.region_coords[key], {
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

                this.featureGroup.addLayer(circle);
                this.styleCircle(circle, xval, { type: "region", id: key });
              }
            );
          } else if (this.current_zoom < ZOOM_LEVEL.DEAL_CLUSTERS && Object.keys(this.country_coords).length) {
            // cluster by country
            Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
              ([key, val]) => {
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
                this.featureGroup.addLayer(circle);
                this.styleCircle(circle, val.length, { type: "country", id: key });
              }
            );
          } else {
            // cluster deals with markercluster
            Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
              ([key, val]) => {
                let mcluster = L.markerClusterGroup({
                  //disableClusteringAtZoom: ZOOM_LEVEL.DEAL_PINS, // spiderfy will not work anymore :(
                  chunkedLoading: true,
                  // iconCreateFunction: function (cluster) {
                  //   return L.divIcon({
                  //     html: `<span class='landmatrix-custom-circle'>${cluster.getChildCount()} deals</span>`,
                  //
                  //   });
                  // },
                });
                mcluster.on("clusterclick", (a) => {
                  let bounds = a.layer.getBounds().pad(0.5);
                  this.bigmap.fitBounds(bounds);
                });
                val.forEach((mark) => mcluster.addLayer(mark));
                this.featureGroup.addLayer(mcluster);
              }
            );
            // this.markers.forEach((mark) => {
            //   this.featureGroup.addLayer(mark);
            // });
          }
        }
      },
      pinTheMap(bigmap) {
        console.log("Pinning the map")
        this.bigmap = bigmap;
        this.bigmap.addLayer(this.featureGroup);
        this.bigmap.addLayer(this.contextLayersLayerGroup);
        bigmap.on("zoomend", (e) => (this.current_zoom = bigmap.getZoom()));
      },
      getPopupHtml(deal, loc) {
        let template = document.createElement('template');
        let popupHtml = `<div class="deal-popup">
          <h3>Deal #${deal.id}</h3>
          <div class="deal-summary">
            <dl>
              <dt>Spatial accuracy</dt><dd>${getFieldValue(
                loc,
                this.formfields,
                "level_of_accuracy",
                "location"
              )}</dd>
              <dt>Intention of investment</dt><dd>${getFieldValue(
                deal,
                this.formfields,
                "current_intention_of_investment"
              )}</dd>
              <dt>Deal size</dt><dd>${getDealValue(
                this,
                deal,
                "deal_size"
              )}</dd>
              <dt>Operating company</dt><dd>
                 ${getDealValue(this, deal, "operating_company")}
              </dd>
            </dl>
          </div>
          <a class="btn btn-primary" target="_blank" href="/newdeal/deal/${
            deal.id
          }">More details</a>
        </div>`;
        template.innerHTML = popupHtml.trim();
        return template.content.firstChild;
      },
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.$store.dispatch("showScopeOverlay", true);
      });
    },
  };
</script>
<style lang="scss">
  @import "../../scss/colors";

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
      z-index: 500 !important;

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
