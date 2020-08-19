<template>
  <div class="container mh-100" style="max-width: 100%;">
    <div class="row">
      <div class="col" style="min-height: 700px; border: 1px solid; padding: 0;">
        <big-map
          :options="bigmap_options"
          :containerStyle="{ 'max-height': '100%', height: '100%' }"
          @ready="pinTheMap"
        >
          <template v-slot:overlay>
            <FilterBar :deals="deals"></FilterBar>
            <div class="scope-overlay" :class="{ collapsed: !showScopeOverlay }">
              <div class="toggle-button">
                <a href="#" @click.prevent="showScopeOverlay = !showScopeOverlay">
                  <i
                    class="fas"
                    :class="[showScopeOverlay ? 'fa-chevron-left' : 'fa-chevron-right']"
                  ></i>
                </a>
              </div>
              <div class="overlay-content">
                asdf
              </div>
            </div>
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
  // import { PruneCluster, PruneClusterForLeaflet } from "prunecluster-exportable/dist";
  import { groupBy } from "lodash";
  import FilterBar from "../components/Map/FilterBar";

  export default {
    name: "GlobalMap",
    components: { FilterBar, BigMap },
    apollo: {
      deals: {
        query: gql`
          query Deals($limit: Int!) {
            deals(limit: $limit) {
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
        variables: {
          limit: 200,
        },
      },
    },
    data() {
      return {
        bigmap_options: { zoom: 2, zoomControl: false, gestureHandling: false },
        showFilterOverlay: true,
        showScopeOverlay: false,
        deals: [],
        bigmap: null,
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
        // // console.log(this.bigmap);
        // var layers = [];
        // this.bigmap.eachLayer(function (layer) {
        //   // console.log(layer._url);
        //   if (layer instanceof L.TileLayer)
        //     // console.log(layer._url);
        //     layers.push(layer);
        // });
        // console.log(layers);
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

<style lang="scss">
  .scope-overlay {
    position: absolute;
    background-color: rgba(255, 255, 255, 0.95);
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 10;
    display: flex;
    .toggle-button {
      position: absolute;
      left: 10px;
    }
    .overlay-content {
      width: 20vw;
      max-width: 230px;
      height: 100%;
      overflow-y: auto;
      padding: 0.5em;
    }
    &.collapsed {
      width: 25px;
      .toggle-button {
        position: static;
      }
      .overlay-content {
        display: none;
      }
    }
  }
</style>
