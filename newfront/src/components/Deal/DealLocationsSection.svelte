<script lang="ts">
  import { area } from "@turf/turf";
  import type { Layer, Map } from "leaflet";
  import { GeoJSON, LatLngBounds } from "leaflet?client";
  import type { Deal } from "$lib/types/deal";
  import BigMap from "$components/Map/BigMap.svelte";
  import DealSubmodelSection from "./DealSubmodelSection.svelte";

  export let deal: Deal;

  let bigmap: Map;
  let layer: Layer;

  let styles = {
    contract_area: { dashArray: "5, 5", dashOffset: "0", fillColor: "#ff00ff" },
    intended_area: { dashArray: "5, 5", dashOffset: "0", fillColor: "#66ff33" },
    production_area: { fillColor: "#ff0000" },
  };

  let geojson_options = {
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

      tooltip += `<div class="font-bold">Location #${feature.properties.id}</div>
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

      layer.bindPopup(tooltip, { permanent: false, sticky: true, keepInView: true });
      layer.on("mouseover", () => layer.openPopup());
      layer.on("mouseout", () => layer.closePopup());
    },
  };

  //   watch: {
  //     deal() {
  //       this.refreshMap();
  //     },
  //   },

  async function refreshMap() {
    if (!(deal && deal.country && bigmap)) return;

    if (layer) {
      bigmap.removeLayer(layer);
    }
    layer = new GeoJSON(deal.geojson, geojson_options);
    let mybounds = layer.getBounds();
    let ne = mybounds.getNorthEast();
    let sw = mybounds.getSouthWest();
    if (ne && sw) {
      if (ne.equals(sw)) {
        ne.lat += 10;
        ne.lng += 10;
        sw.lat -= 10;
        sw.lng -= 10;
        bigmap.fitBounds(new LatLngBounds(ne, sw), { animate: false });
      }
      bigmap.fitBounds(mybounds.pad(1.2), { animate: false });
    }
    bigmap.addLayer(layer);
  }

  const onMapReady = async (event: CustomEvent<Map>) => {
    bigmap = event.detail;
    await refreshMap();
  };
</script>

<DealSubmodelSection model="location" modelName="Location" entries={deal.locations}>
  <div class="min-h-[20rem] w-full lg:w-1/2">
    <BigMap
      containerClass="min-h-full h-full mt-5"
      options={{ center: [0, 0] }}
      on:ready={onMapReady}
    />
  </div>
</DealSubmodelSection>

<!--<style lang="scss">-->
<!--  .locations {-->
<!--    .map-container {-->
<!--      min-height: 250px;-->

<!--      #bigMap {-->
<!--        max-height: 50vh;-->
<!--        margin-top: 2em;-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--</style>-->
