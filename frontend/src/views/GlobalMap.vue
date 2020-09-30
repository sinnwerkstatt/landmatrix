<template>
  <div class="container" style="max-height: 90%; max-width: 100%;">
    <div class="row">
      <div
        class="col"
        style="min-height: 500px; height: 70vh; border: 1px #6c757d dotted; padding: 0;"
      >
        <BigMap
          :options="bigmap_options"
          :center="[12,30]"
          :containerStyle="{ 'max-height': '100%', height: '100%' }"
          @ready="pinTheMap"
          :hideLayerSwitcher="true"
        >
          <div
            v-if="$apollo.queries.deals.loading"
            style="
              font-size: 20px;
              z-index: 500000;
              position: absolute;
              bottom: 10px;
              left: 50%;
            "
          >
            Loading...
          </div>
        </BigMap>
        <FilterBar :deals="deals">
          <h4>{{ $t("Map settings") }}</h4>
          <FilterCollapse title="Displayed Data">
            <label>
              <input type="radio" v-model="displayHectares" :value="false" />
              Number of deals
            </label>
            <label style="color: gray !important;">
              <input disabled type="radio" v-model="displayHectares" :value="true" />
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
    <!--    {{ this.$store.state.filters.filters }}-->
    <!--    <hr />-->
    <!--    {{ this.$store.getters.filtersForGQL }}-->
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
            filters: this.$store.getters.filtersForGQL,
          };
        },
      },
    },
    data() {
      return {
        bigmap_options: {
          minZoom: 2,
          zoom: 3,
          zoomControl: false,
          gestureHandling: false,
        },
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
      styleCircle(circle, size, country_or_region_with_id) {
        let circle_elem = circle.getElement();
        let innertext = document.createElement("span");
        innertext.className = "landmatrix-custom-circle-text";
        innertext.innerHTML = `${size} deals`;
        circle_elem.append(innertext);
        let factor = Math.max(Math.log(size) * 16, 40);
        Object.assign(circle_elem.style, {
          height: `${factor}px`,
          width: `${factor}px`,
          background: primary_color,
        });
        let tooltip = document.createElement("span");
        tooltip.className = "landmatrix-custom-circle-hover-text";
        let coun_reg = this.$store.getters.getCountryOrRegion(
          country_or_region_with_id
        );
        if (coun_reg) tooltip.innerHTML = coun_reg.name;
        circle_elem.append(tooltip);
      },
      refreshMap() {
        if (this.bigmap && this.markers) {
          this.featureGroup.clearLayers();
          if (this.current_zoom < 3) {
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

                this.featureGroup.addLayer(circle);
                this.styleCircle(circle, val.length, { type: "region", id: key });
              }
            );
          } else if (this.current_zoom < 6) {
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
            Object.entries(groupBy(this.markers, (mark) => mark.country_id)).forEach(
              ([key, val]) => {
                let mcluster = L.markerClusterGroup();
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
      .landmatrix-custom-circle-hover-text {
        display: inline;
      }
    }
  }

  .leaflet-marker-icon .leaflet-div-icon {
  }
</style>
