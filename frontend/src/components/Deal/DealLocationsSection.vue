<template>
  <DealSubmodelSection
    title="Locations"
    model-name="Location"
    :entries="deal.locations"
    :fields="fields"
    model="location"
    :active="active"
    :label-classes="['display-field-label', 'col-md-6']"
    :value-classes="['display-field-value', 'col-md-6']"
    @activated="activateTab"
  >
    <div class="locations col-md-12 col-lg-5 col-xl-6">
      <BigMap
        :container-style="{ 'max-height': '90%', height: '90%' }"
        :center="[0, 0]"
        @ready="mapIsReady"
      />
    </div>
  </DealSubmodelSection>
</template>

<script>
  import BigMap from "$components/BigMap";

  import { area } from "@turf/turf";
  import { GeoJSON, LatLngBounds } from "leaflet";
  import DealSubmodelSection from "./DealSubmodelSection";

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

  export default {
    components: {
      DealSubmodelSection,
      BigMap,
    },
    props: {
      fields: { type: Array, required: true },
      deal: { type: Object, required: true },
      active: { type: Boolean, default: false },
    },
    data() {
      return {
        bigmap: null,
        layer: null,
        geojson_options: {
          style: (feature) => {
            return {
              weight: 2,
              color: "#000000",
              opacity: 1,
              fillOpacity: 0.2,
              ...styles[feature.properties.type],
            };
          },
          onEachFeature: (feature, layer) => {
            let tooltip = "<div>";

            tooltip += `<div>Location #${feature.properties.id}</div>
                      <div>Name: ${feature.properties.name}</div>
                      <div>Type: ${feature.properties.type}</div>`;

            if (feature.geometry.type !== "Point") {
              let farea = (area(layer.toGeoJSON()) / 10000)
                .toFixed(2)
                .toString()
                .replace(/\B(?=(\d{3})+(?!\d))/g, " ");
              tooltip += `<div>Area: ${farea} ha</div>`;
            }
            tooltip += "</div>";

            layer.bindPopup(tooltip, {
              permanent: false,
              sticky: true,
              keepInView: true,
            });
            layer.on("mouseover", () => layer.openPopup());
            layer.on("mouseout", () => layer.closePopup());
          },
        },
      };
    },
    watch: {
      deal() {
        this.refreshMap();
      },
    },
    methods: {
      activateTab() {
        this.$emit("activated");
        this.$nextTick(() => this.bigmap.invalidateSize());
      },
      refreshMap() {
        if (this.deal && this.deal.country && this.bigmap) {
          console.log(this.deal.geojson);
          if (this.layer) {
            this.bigmap.removeLayer(this.layer);
          }
          console.log(this.deal.geojson);
          this.layer = new GeoJSON(this.deal.geojson, this.geojson_options);
          let mybounds = this.layer.getBounds();
          let ne = mybounds.getNorthEast();
          let sw = mybounds.getSouthWest();
          if (ne && sw) {
            if (ne.equals(sw)) {
              ne.lat += 10;
              ne.lng += 10;
              sw.lat -= 10;
              sw.lng -= 10;
              this.bigmap.fitBounds(new LatLngBounds(ne, sw), { animate: false });
            }
            this.bigmap.fitBounds(mybounds.pad(1.2), { animate: false });
          }
          this.bigmap.addLayer(this.layer);
        }
      },
      mapIsReady(map) {
        this.bigmap = map;
        this.refreshMap();
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
