<template>
  <div v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="Location" active>
        <div style="height: 500px; width: 100%;">
          <l-map
            :bounds="bounds"
            :options="mapOptions"
            style="height: 80%;"
            ref="dealMap"
          >
            <l-control-layers position="topright"></l-control-layers>
            <l-tile-layer
              v-for="tileProvider in tileProviders"
              :key="tileProvider.name"
              :name="tileProvider.name"
              :visible="tileProvider.visible || false"
              :url="tileProvider.url"
              :attribution="tileProvider.attribution"
              :maxZoom="tileProvider.maxZoom || 19"
              layer-type="base"
            />
            <l-geo-json
              v-if="deal.geojson"
              :geojson="deal.geojson"
              :options="geojson_options"
              :optionsStyle="geojson_styleFunction"
            />
          </l-map>
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
  import store from "../store";

  export default {
    // name: 'Deal',
    props: ["deal_id"],
    data() {
      return {
        mapOptions: {
          zoomSnap: 0.5,
        },
        tileProviders: [
          {
            name: "OpenStreetMap",
            visible: true,
            attribution:
              '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          },
          {
            name: "CartoDB Positron",
            url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            attribution:
              '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
          },
          {
            name: "ESRI Satellite",
            url:
              "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attribution:
              "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
          },
          {
            name: "ESRI Topology",
            url:
              "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
            attribution:
              "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community",
          },
          {
            name: "OpenTopoMap",
            maxZoom: 17,
            url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            attribution:
              'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
          },
        ],
      };
    },
    computed: {
      deal() {
        return this.$store.state.current_deal;
      },
      bounds() {
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
        breadcrumbs: [{ href: "/newdeal/", name: "Data" }, { name: title }],
      });
      next();
    },
    beforeRouteLeave(to, from, next) {
      store.dispatch("setCurrentDeal", null);
      next();
    },
  };
</script>
