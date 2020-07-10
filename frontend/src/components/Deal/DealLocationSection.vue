<template>
  <b-tab :title="title" active>
    <div class="row">
      <div class="col">
        <div v-for="location in deal.locations" class="panel-body">
          <h3>{{title}} #{{ location.id }}</h3>
          <dl class="row mt-3">
            <template
              v-for="formfield in fields"
              :class="formfield.name"
              v-if="!readonly || custom_is_null(location[formfield.name])"
            >
              <dt class="col-md-3" :key="`dt-${formfield.name}`">
                {{ formfield.label }}
              </dt>
              <dd class="col-md-9" :key="`dd-${formfield.name}`">
                <component
                  :is="formfield.class"
                  :formfield="formfield"
                  :readonly="!!readonly"
                  v-model="location[formfield.name]"
                ></component>
              </dd>
            </template>
          </dl>
        </div>
      </div>
      <div class="col">
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
    </div>
  </b-tab>
</template>

<script>
  import CharField from "/components/Fields/TextField";
  import TextField from "/components/Fields/TextField";
  import PointField from "/components/Fields/PointField";
  import BigMap from "../BigMap";
  import { LGeoJson } from "vue2-leaflet";

  export default {
    props: ["title", "fields", "deal", "readonly"],
    components: {
      CharField,
      PointField,
      TextField,
      BigMap,
      LGeoJson,
    },
    computed: {
      bounds() {
        if (!this.deal) return null;
        let mybounds = L.geoJSON(this.deal.geojson).getBounds();

        let ne = mybounds.getNorthEast();
        let sw = mybounds.getSouthWest();
        if (ne.equals(sw)) {
          ne.lat += 10;
          ne.lng += 10;
          sw.lat -= 10;
          sw.lng -= 10;
          return L.latLngBounds(ne, sw);
        }
        return mybounds.pad(1.5);
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
    },
    methods: {
      custom_is_null(field) {
        return !(
          field === undefined ||
          field === null ||
          field === "" ||
          (Array.isArray(field) && field.length === 0)
        );
      },
    },
  };
</script>
