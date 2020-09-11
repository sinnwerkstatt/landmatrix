<template>
  <div class="container" style="max-height: 90%; max-width: 100%;">
    <div class="row">
      <div
        class="col"
        style="min-height: 500px; height: 70vh; border: 1px #6c757d dotted; padding: 0;"
      >
        <BigMap
          :options="bigmap_options"
          :containerStyle="{ 'max-height': '100%', height: '100%' }"
          @ready="pinTheMap"
          :hideLayerSwitcher="true"
        />
        <FilterBar :deals="deals">
          <h4>{{ $t("Map settings") }}</h4>
          <FilterCollapse title="Displayed Data">
            <label>
              <input type="radio" v-model="displayHectares" :value="false" />
              Number of deals
            </label>
            <label>
              <input type="radio" v-model="displayHectares" :value="true" />
              Area (ha)
            </label>
          </FilterCollapse>
          <FilterCollapse title="Base layer">
            <ul class="layer-list">
              <li v-for="layer in tileLayers">
                <div v-if="layer.name === visibleLayer">{{ layer.name }}</div>
                <a
                  v-else
                  @click.prevent="$store.dispatch('setCurrentLayer', layer.name)"
                >
                  {{ layer.name }}
                </a>
              </li>
            </ul>
          </FilterCollapse>
        </FilterBar>
        <ScopeBar></ScopeBar>
      </div>
    </div>
  </div>
</template>

<script>
  import BigMap from "/components/BigMap";
  import gql from "graphql-tag";
  import "leaflet";
  import "leaflet.markercluster";
  import { groupBy } from "lodash";
  import FilterBar from "../components/Map/FilterBar";
  import ScopeBar from "../components/Map/ScopeBar";
  import FilterCollapse from "../components/Map/FilterCollapse";
  import { mapState } from "vuex";
  import { primary_color } from "../colors";

  export default {
    name: "GlobalMap",
    components: { FilterCollapse, ScopeBar, FilterBar, BigMap },
    apollo: {
      deals: {
        query: gql`
          query Deals($limit: Int!, $filters: [Filter]) {
            deals(limit: $limit, filters: $filters) {
              id
              deal_size
              country {
                id
                fk_region {
                  id
                }
              }
              # top_investors { id name }
              intention_of_investment
              current_negotiation_status
              current_implementation_status
              locations {
                id
                point
                level_of_accuracy
              }
            }
          }
        `,
        variables() {
          return {
            limit: 0,
            filters: this.$store.state.filters.filters,
          };
        },
      },
    },
    data() {
      return {
        bigmap_options: { zoom: 2, zoomControl: false, gestureHandling: false },
        deals: [],
        bigmap: null,
        current_zoom: 2,
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
      ...mapState({
        tileLayers: (state) => state.map.layers,
        visibleLayer: (state) => state.map.visibleLayer,
        country_coords: (state) => {
          let coords = {};
          state.page.countries.forEach((country) => {
            coords[country.id] = [country.point_lat, country.point_lon];
          });
          return coords;
        },
        markers() {
          let markers = [];
          this.deals.map((deal) => {
            deal.locations.map((loc) => {
              if (loc.point) {
                let marker = new L.marker([loc.point.lat, loc.point.lng]);
                marker.deal_id = deal.id;
                if (deal.country) {
                  marker.region_id = deal.country.fk_region.id;
                  marker.country_id = deal.country.id;
                }
                marker.on("click", (e) => console.log(e.target.deal_id));
                markers.push(marker);
              }
            });
          });
          return markers;
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
    },
    methods: {
      refreshMap() {
        if (this.bigmap && this.markers) {
          if (this.current_zoom < 3) {
            this.featureGroup.clearLayers();
            Object.entries(groupBy(this.markers, (mark) => mark.region_id)).forEach(
              ([key, val]) => {
                let radius = Math.log(val.length) * 5 * this.current_zoom;
                let circle = L.circleMarker(this.region_coords[key], {
                  stroke: false,
                  fillColor: primary_color,
                  fillOpacity: 0.9,
                  radius,
                  region_id: key,
                });
                circle.on("click", (e) => console.log(e.target.options.region_id));
                this.featureGroup.addLayer(circle);
              }
            );
          } else if (this.current_zoom < 5) {
            this.featureGroup.clearLayers();
            Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
              ([key, val]) => {
                let radius = Math.log(val.length) * 2.5 * this.current_zoom;
                let circle = L.circleMarker(this.country_coords[key], {
                  stroke: false,
                  fillColor: primary_color,
                  fillOpacity: 0.9,
                  radius,
                  country_id: key,
                });
                circle.on("click", (e) => console.log(e.target.options.country_id));
                this.featureGroup.addLayer(circle);
              }
            );
          } else {
            this.featureGroup.clearLayers();
            this.markers.forEach((mark) => {
              this.featureGroup.addLayer(mark);
            });
          }
        }
      },
      pinTheMap(bigmap) {
        this.bigmap = bigmap;
        this.bigmap.addLayer(this.featureGroup);
        bigmap.on("zoomend", (e) => (this.current_zoom = bigmap.getZoom()));
      },
    },
  };
</script>
