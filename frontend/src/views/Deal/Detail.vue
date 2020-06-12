<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="Location">
        <div>
          <big-map
            :containerStyle="{ 'max-height': '300px', height: '300px' }"
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

      <b-tab title="General Info" active>
        <div v-for="section in general_info" class="panel-body">
          <h3>{{ section.name }}</h3>
          <div
            v-for="formfield in section.fields"
            :key="formfield.name"
            :class="['row', 'mt-3', formfield.name]"
            v-if="deal[formfield.name]"
          >
            <div class="col-md-3">
              {{ formfield.label }}
            </div>
            <div class="col-md-9">
              <component
                :is="formfield.component"
                :formfield="formfield"
                :readonly="true"
                v-model="deal[formfield.name]"
              ></component>
            </div>
          </div>
        </div>
      </b-tab>

      <b-tab title="Employment"><p></p></b-tab>
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
  import TextField from "@/components/Fields/TextField";
  import ValueDateField from "@/components/Fields/ValueDateField";

  import { LGeoJson } from "vue2-leaflet";
  import { general_info } from "./deal_fields";
  import CheckboxField from "@/components/Fields/CheckboxField";

  export default {
    props: ["deal_id"],
    components: { BigMap, LGeoJson, TextField, ValueDateField, CheckboxField },
    data() {
      return {
        general_info: general_info,
      };
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
          pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
              radius: 8,
            });
          },
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
          let tooltip = `<div>
                <div>ID: ${feature.properties.id}</div>
                <div>Name: ${feature.properties.name}</div>
                <div>Type: ${feature.properties.type}</div>
            </div>`;
          layer.bindTooltip(tooltip, { permanent: false, sticky: true });
        };
      },
    },
    methods: {},
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
