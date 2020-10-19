<template>
  <div>
    <DataContainer>
      <template v-slot:default>
        <LoadingPulse v-if="$apollo.queries.deals.loading"/>
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
        <FilterCollapse title="Displayed Data">
          <b-form-group>
            <b-form-radio
              v-model="displayHectares"
              name="displayHectaresRadio"
              :value="false"
            >
              {{ $t("Number of deals") }}
            </b-form-radio>
            <b-form-radio
              v-model="displayHectares"
              name="displayHectaresRadio"
              :value="true"
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
      </template>
    </DataContainer>
  </div>
</template>

<script>
import "leaflet";
import "leaflet.markercluster";
import {groupBy} from "lodash";
import {mapState} from "vuex";
import {primary_color} from "/colors";

import BigMap from "/components/BigMap";
import DataContainer from "./DataContainer";
import FilterCollapse from "/components/Data/FilterCollapse";
import LoadingPulse from "/components/Data/LoadingPulse";
import {data_deal_query} from "./query";

const ZOOM_LEVEL = {
  REGION_CLUSTERS: 2,
  COUNTRY_CLUSTERS: 3,
  DEAL_CLUSTERS: 5,
}

export default {
  name: "GlobalMap",
  components: {LoadingPulse, FilterCollapse, DataContainer, BigMap},
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
      deals: [],
      bigmap: null,
      current_zoom: ZOOM_LEVEL.REGION_CLUSTERS,
      featureGroup: L.featureGroup(),
      displayHectares: false,
      region_coords: {
        2: [6.06433, 17.082249],
        9: [-22.7359, 140.0188],
        21: [54.526, -105.2551],
        142: [34.0479, 100.6197],
        150: [52.0055, 37.9587],
        419: [-4.442, -61.3269],
      },
    };
  },
  computed: {
    visibleLayer: {
      get() {
        return this.$store.state.map.visibleLayer;
      },
      set(value) {
        this.$store.dispatch("setCurrentLayer", value);
      },
    },
    ...mapState({
      tileLayers: (state) => state.map.layers,
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
        let markers_list = [];
        this.deals.map((deal) => {
          deal.locations.map((loc) => {
            if (loc.point) {
              let marker = new L.marker([loc.point.lat, loc.point.lng]);
              marker.deal_id = deal.id;
              marker.deal_size = deal.deal_size;
              if (deal.country) {
                marker.region_id = deal.country.fk_region.id;
                marker.country_id = deal.country.id;
              }
              // marker.on("click", (e) => console.log(e.target.deal_id));
              let popupHtml = `
                  <h2>Deal #${deal.id}</h2>
                  <a href="/newdeal/deal/${deal.id}">More details</a>
                `;
              marker.bindPopup(popupHtml);
              markers_list.push(marker);
            }
          });
        });
        return markers_list;
      },
    }),
  },
  watch: {
    deals() {
      this.refreshMap();
    },
    markers() {
      this.refreshMap();
    },
    bigmap() {
      this.refreshMap();
    },
    current_zoom() {
      this.refreshMap();
    },
    displayHectares() {
      this.refreshMap();
    },
    '$store.state.page.regions': function () {
      // otherwise country name will not be displayed on initial load with small list of
      // filtered deals (e.g. single country)
      // TODO: Make sure that countries/regions are loaded before deals?!
      this.refreshMap();
    },
    region_id() {
      this.flyToCountryOrRegion();
    },
    country_id() {
      this.flyToCountryOrRegion();
    }
  },
  methods: {
    flyToCountryOrRegion() {
      if (this.country_id) {
        this.bigmap.flyTo(this.country_coords[this.country_id], ZOOM_LEVEL.DEAL_CLUSTERS);
      } else if (this.region_id) {
        this.bigmap.flyTo(this.region_coords[this.region_id], ZOOM_LEVEL.COUNTRY_CLUSTERS);
      } else {
        this.bigmap.flyTo([0,0], ZOOM_LEVEL.REGION_CLUSTERS);
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
      if (this.displayHectares) {
        hoverlabel.innerHTML = `${size} hectares`;
        factor = Math.max(Math.log(size) * 6, 40);
      } else {
        hoverlabel.innerHTML = `${size} deals`;
        factor = Math.max(Math.log(size) * 16, 40);
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
      this.featureGroup.clearLayers();
      if (this.bigmap && this.markers.length > 0) {
        this.current_zoom = this.bigmap.getZoom();
        if (this.current_zoom < ZOOM_LEVEL.COUNTRY_CLUSTERS && !this.country_id) {
          // cluster by Region
          Object.entries(groupBy(this.markers, (mark) => mark.region_id)).forEach(
            ([key, val]) => {
              let circle = L.marker(this.region_coords[key], {
                icon: L.divIcon({className: "landmatrix-custom-circle"}),
                region_id: key,
              });
              circle.on("click", (e) => {
                this.$store.dispatch("setFilter", {
                  filter: "region_id",
                  value: +e.target.options.region_id,
                });
              });

              let xval;
              if (this.displayHectares) {
                xval = val.reduce((x, y) => {
                  return {deal_size: x.deal_size + y.deal_size};
                }).deal_size;
              } else {
                xval = val.length;
              }

              this.featureGroup.addLayer(circle);
              this.styleCircle(circle, xval, {type: "region", id: key});
            }
          );
        } else if (this.current_zoom < ZOOM_LEVEL.DEAL_CLUSTERS) {
          // cluster by country
          Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
            ([key, val]) => {
              let circle = L.marker(this.country_coords[key], {
                icon: L.divIcon({className: "landmatrix-custom-circle"}),
                country_id: key,
              });
              circle.on("click", (e) => {
                this.$store.dispatch("setFilter", {
                  filter: "country_id",
                  value: +e.target.options.country_id,
                });
              });
              this.featureGroup.addLayer(circle);
              this.styleCircle(circle, val.length, {type: "country", id: key});
            }
          );
        } else {
          // cluster deals with markercluster
          Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
            ([key, val]) => {
              let mcluster = L.markerClusterGroup({
                // iconCreateFunction: function (cluster) {
                //   return L.divIcon({
                //     html: `<span class='landmatrix-custom-circle'>${cluster.getChildCount()} deals</span>`,
                //
                //   });
                // },
              });
              mcluster.on('clusterclick', (a) => {
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
      this.bigmap = bigmap;
      this.bigmap.addLayer(this.featureGroup);
      bigmap.on("zoomend", (e) => (this.current_zoom = bigmap.getZoom()));
    },
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.$store.dispatch("showScopeOverlay", true);
    })
  },
};
</script>
<style lang="scss">
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
      background-color: rgba(252, 215, 172, 0.8)
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

</style>
