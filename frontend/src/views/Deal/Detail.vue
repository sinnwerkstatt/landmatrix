<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="Location" active>
        <div v-if="deal">
          <big-map
            :containerStyle="{'max-height':'300px', 'height': '300px'}"
            :bounds="bounds"
          >
            <l-geo-json
              v-if="deal.geojson"
              :geojson="deal.geojson"
              :options="geojson_options"
              :optionsStyle="geojson_styleFunction"
            />
          </big-map>
        </div>
      </b-tab>

      <b-tab title="General Info">
        <div v-for="(v, k) in general_info(deal)">
          <h3>{{ k }}</h3>
          <p>{{ v }}</p>
        </div>
      </b-tab>

      <b-tab title="Employment"> <p></p></b-tab>
    </b-tabs>
  </div>
</template>

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }
</style>
<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";
  import { LGeoJson } from "vue2-leaflet";

  export default {
    props: ["deal_id"],
    components: {BigMap, LGeoJson},
    data() {
      return {}
    },
    computed: {
      deal() {
        return this.$store.state.deal.current_deal;
      },
      bounds() {
        if (!this.deal) return null;
        console.log(this.deal);
        return L.latLngBounds(L.geoJSON(this.deal.geojson).getBounds()).pad(1.5);
      },
      geojson_options() {
        return {
          onEachFeature: this.onEachFeatureFunction,
        };
      },
      geojson_styleFunction() {
        let styles = {
          contract_area: {
            dashArray: "5, 5",
            dashOffset: "0",
            fillColor: "#ffec03",
          },
          intended_area: {
            dashArray: "5, 5",
            dashOffset: "0",
            fillColor: "#ff8900",
          },
          production_area: {
            fillColor: "#ff0000",
          },
        };
        return (feature, layer) => {
          return {
            weight: 2,
            color: "#000000",
            opacity: 1,
            fillOpacity: 0.2,
            ...styles[feature.properties.type],
          };
        };
      },
      onEachFeatureFunction() {
        return (feature, layer) => {
          layer.bindTooltip(
            `<div>Name: ${feature.properties.name}</div>` +
              `<div>Type: ${feature.properties.type}</div>`,
            { permanent: false, sticky: true }
          );
        };
      },
    },
    methods: {
      general_info(deal) {
        return deal;
      },
    },
    beforeRouteEnter(to, from, next) {
      let title = `Deal #${to.params.deal_id}`;
      store.dispatch("setCurrentDeal", to.params.deal_id);
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "deal_list" }, name: "Data" },
          { name: title },
        ],
      });
      next();
    },
    beforeRouteLeave(to, from, next) {
      store.dispatch("setCurrentDeal", {});
      next();
    },
  };
</script>
