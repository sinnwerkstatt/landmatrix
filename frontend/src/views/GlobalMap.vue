<template>
  <div class="container">
    <div v-html="map_introduction"></div>
    <FilterBar />
    <big-map :options="{ zoom: 2 }" @ready="pinTheMap"> </big-map>
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";
  import FilterBar from "@/components/FilterBar";
  import axios from "axios";

  import "leaflet";
  import "leaflet.markercluster";
  import "leaflet.markercluster/dist/MarkerCluster.css";

  export default {
    name: "GlobalMap",
    components: { BigMap, FilterBar },
    data() {
      return {
        locations: null,
        bigmap: null,
      };
    },
    computed: {
      map_introduction() {
        if (this.$store.state.wagtailRootPage)
          return this.$store.state.wagtailRootPage.map_introduction;
      },
    },
    methods: {
      pinTheMap(x) {
        this.bigmap = x;
        if (this.locations) this.addTheMarkers();
      },
      addTheMarkers() {
        var markers = L.markerClusterGroup();
        this.locations.map((loc) => {
          if(loc.point) {
            markers.addLayer(L.marker(loc.point));
          }
        });

        this.bigmap.addLayer(markers);
      }
    },
    created() {
      let query = `{ locations(limit: 0) { id point { lat lon } level_of_accuracy deal { id } } }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        this.locations = response.data.data.locations;
        if(this.bigmap) this.addTheMarkers();
      });

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

<style lang="scss" scoped></style>
