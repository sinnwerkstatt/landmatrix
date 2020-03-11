<template>
  <div v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="Location" active>
        <div style="height: 500px; width: 100%">
          <l-map
              :bounds="bounds"
              :options="mapOptions"
              style="height: 80%"
              ref="dealMap"
          >
            <l-tile-layer
                :url="url"
                :attribution="attribution"
            />

            <l-feature-group>
              <l-geo-json v-if="geojson"
                          :geojson="geojson"
                          :options="geojson_options"
                          :optionsStyle="geojson_styleFunction"
              />
            </l-feature-group>
          </l-map>
        </div>
      </b-tab>

      <b-tab title="General Info">
        <div v-for="(v,k) in deal.general_info">
          <h3>{{k}}</h3>
          <p>{{v}}</p>
        </div>
      </b-tab>

      <b-tab title="Employment">
        <p></p></b-tab>
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
  import store from '../store';

  export default {
    // name: 'Deal',
    props: ['deal_id'],
    data() {
      return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution:
            '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        mapOptions: {
          zoomSnap: 0.5
        },
      };
    },
    computed: {
      deal() {
        return this.$store.state.current_deal
      },
      geojson() {
        return this.deal.geojson;
      },
      bounds() {
        return L.latLngBounds(L.geoJSON(this.deal.geojson).getBounds()).pad(1.5);
      },
      geojson_options() {
        return {
          onEachFeature: this.onEachFeatureFunction
        };
      },
      geojson_styleFunction() {
        let styles = {
          contract_area: {
            dashArray: '5, 5',
            dashOffset: '0',
            fillColor: "#ffec03",
          },
          intended_area: {
            dashArray: '5, 5',
            dashOffset: '0',
            fillColor: "#ff8900",
          },
          production_area: {
            fillColor: "#ff0000",
          }
        };
        return (feature, layer) => {
          return {
            weight: 2,
            color: "#000000",
            opacity: 1,
            fillOpacity: 0.2,
            ...styles[feature.properties.type]
          };
        };
      },
      onEachFeatureFunction() {
        return (feature, layer) => {
          layer.bindTooltip(`<div>Name: ${feature.properties.name}</div>` +
              `<div>Type: ${feature.properties.type}</div>`,
              {permanent: false, sticky: true}
          );
        };
      }
    },
    beforeRouteEnter(to, from, next) {
      store.dispatch('setTitle', `Deal #${to.params.deal_id}`);
      store.dispatch('setCurrentDeal', to.params.deal_id);
      next()
    },
    beforeRouteLeave(to, from, next) {
      store.dispatch('setCurrentDeal', null);
      next()
    },
  }
  ;
</script>
