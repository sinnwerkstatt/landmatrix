<template>
  <DealSubmodelSection
    :title="$t('Locations')"
    :model-name="$t('Location')"
    :entries="entries"
    :fields="fields"
    model="location"
    :active="active"
    :label-classes="['display-field-label', 'col-md-6']"
    :value-classes="['display-field-value', 'col-md-6']"
    @activated="$emit('activated')"
  >
    <div class="locations col-md-12 col-lg-5 col-xl-6">
      <big-map
        :container-style="{ 'max-height': '90%', height: '90%' }"
        :bounds="bounds"
      >
        <l-geo-json
          v-if="deal.geojson"
          :geojson="deal.geojson"
          :options="geojson_options"
          :options-style="geojson_styleFunction"
        />
      </big-map>
    </div>
  </DealSubmodelSection>
</template>

<script>
  import BigMap from "components/BigMap";
  import { LGeoJson } from "vue2-leaflet";
  import { GeoJSON, LatLngBounds } from "leaflet";
  import DealSubmodelSection from "./DealSubmodelSection";

  export default {
    components: {
      DealSubmodelSection,
      BigMap,
      LGeoJson,
    },
    props: {
      fields: { type: Array, required: true },
      deal: { type: Object, required: true },
      active: { type: Boolean, default: false },
    },
    computed: {
      entries() {
        return this.deal.locations.map((l, index) => {
          return { ...l, loc_no: index + 1, country: this.deal.country.name };
        });
      },
      bounds() {
        if (!this.deal) return null;
        let mybounds = new GeoJSON(this.deal.geojson).getBounds();
        let ne = mybounds.getNorthEast();
        let sw = mybounds.getSouthWest();
        if (!ne || !sw) return null;
        if (ne && ne.equals(sw)) {
          ne.lat += 10;
          ne.lng += 10;
          sw.lat -= 10;
          sw.lng -= 10;
          return new LatLngBounds(ne, sw);
        }
        return mybounds.pad(1.5);
      },
      geojson_options() {
        return {
          onEachFeature: this.onEachFeatureFunction,
          // pointToLayer: function (feature, latlng) {
          //   return L.circleMarker(latlng, {
          //     radius: 8,
          //   });
          // },
        };
      },
      onEachFeatureFunction() {
        return (feature, layer) => {
          let tooltip = `<div>
                  <div>Location #${
                    this.entries.find((l) => l.id === feature.properties.id).loc_no
                  }</div>
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
        return (feature) => {
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

<style lang="scss">
  .locations {
    .map-container {
      min-height: 250px;

      #bigMap {
        max-height: 50vh;
        margin-top: 2em;
      }
    }
  }
</style>
