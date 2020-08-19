<template>
  <div class="container mh-100" style="max-width: 100%;">
    <div class="row">
      <div class="col" style="min-height: 700px; border: 1px solid; padding: 0;">
        <big-map
          :options="bigmap_options"
          :containerStyle="{ 'max-height': '100%', height: '100%' }"
          @ready="pinTheMap"
          :hideLayerSwitcher="true"
        >
          <template v-slot:overlay>
            <FilterBar :deals="deals" :bigmap="bigmap"></FilterBar>
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
            limit: 200,
            filters: this.filters,
          };
        },
      },
    },
    data() {
      return {
        bigmap_options: { zoom: 2, zoomControl: false, gestureHandling: false },
        deals: [],
        bigmap: null,
        filters: [{ field: "deal_size", operation: "GE", value: "200" }],
      };
    },
    watch: {
      deals(newDeals, oldDeals) {
        if (newDeals.length && this.bigmap) {
          this.setMarkers();
        }
      },
    },
    methods: {
      pinTheMap(bigmap) {
        this.bigmap = bigmap;
        if (this.deals.length) this.setMarkers();
      },
      setMarkers() {
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
        let mcg = L.markerClusterGroup({ chunkedLoading: true });
        mcg.addLayers(markers);
        this.bigmap.addLayer(mcg);

        // Object.entries(groupBy(markers, (mark) => mark.country_id)).forEach(
        //   ([key, val]) => {
        //     // let lg = L.layerGroup(val);
        //     // this.bigmap.addLayer(lg);
        //     let mcg = L.markerClusterGroup();
        //     mcg.addLayers(val);
        //     this.bigmap.addLayer(mcg);
        //   }
        // );
      },
    },
  };
</script>
