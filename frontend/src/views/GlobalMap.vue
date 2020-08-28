<template>
  <div class="container mh-100" style="max-width: 100%;">
    {{ this.$store.state.filters.filters }}
    <div class="row">
      <div class="col" style="min-height: 700px; border: 1px solid; padding: 0;">
        <big-map
          :options="bigmap_options"
          :containerStyle="{ 'max-height': '100%', height: '100%' }"
          @ready="pinTheMap"
          :hideLayerSwitcher="true"
        >
          <template v-slot:overlay>
            <FilterBar :deals="deals"></FilterBar>
            <ScopeBar></ScopeBar>
          </template>
        </big-map>
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

  export default {
    name: "GlobalMap",
    components: { ScopeBar, FilterBar, BigMap },
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
              #            intention_of_investment
              #            current_negotiation_status
              #            current_implementation_status
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
            limit: 1000,
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
        markerClusterGroup: L.markerClusterGroup({ chunkedLoading: true }),
      };
    },
    watch: {
      deals(newDeals, oldDeals) {
        if (this.bigmap) {
          let markers = [];
          this.deals.map((deal) => {
            deal.locations.map((loc) => {
              if (loc.point) {
                let marker = new L.marker([loc.point.lat, loc.point.lng]);
                marker.deal_id = deal.id;
                // marker.region_id = deal.country.fk_region.id;
                // marker.country_id = deal.country.id;
                marker.on("click", (e) => console.log(e.target.deal_id));
                markers.push(marker);
              }
            });
          });
          this.markerClusterGroup.clearLayers();
          this.markerClusterGroup.addLayers(markers);
          // Object.entries(groupBy(markers, (mark) => mark.country_id)).forEach(
          //   ([key, val]) => {
          //     // let lg = L.layerGroup(val);
          //     // this.bigmap.addLayer(lg);
          //     let mcg = L.markerClusterGroup();
          //     mcg.addLayers(val);
          //     this.bigmap.addLayer(mcg);
          //   }
          // );
        }
      },
    },
    methods: {
      pinTheMap(bigmap) {
        this.bigmap = bigmap;
        this.bigmap.addLayer(this.markerClusterGroup);
      },
    },
  };
</script>
