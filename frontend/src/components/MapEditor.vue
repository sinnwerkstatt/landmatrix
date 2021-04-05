<template>
  <div class="container">
    <BigMap
      :center="[12, 30]"
      :container-style="{ 'max-height': '600px', height: '600px' }"
      @ready="mapIsReady"
    />
    <form enctype="multipart/form-data" novalidate>
      Upload GeoJSON file
      <input type="file" multiple class="input-file" @change="uploadFiles" />
    </form>
  </div>
</template>

<script>
  import "@geoman-io/leaflet-geoman-free";
  import BigMap from "components/BigMap";
  import { FeatureGroup, GeoJSON } from "leaflet";

  export default {
    components: { BigMap },
    props: { deal: { type: Object, required: true } },
    data() {
      return {
        bigmap: null,
        editableFeatures: new FeatureGroup(),
      };
    },
    methods: {
      features_changed() {
        this.deal.geojson = this.editableFeatures.toGeoJSON();
      },
      mapIsReady(map) {
        this.bigmap = map;
        map.addLayer(this.editableFeatures);
        map.pm.setGlobalOptions({ layerGroup: this.editableFeatures });
        map.pm.addControls({
          position: "topleft",
          drawCircle: false,
          drawCircleMarker: false,
          drawRectangle: false,
          drawPolyline: false,
          cutPolygon: false,
        });

        this.addGeoJson(this.deal.geojson);

        map.on("pm:create", this.features_changed);
        map.on("pm:remove", this.features_changed);
        this.editableFeatures.on("pm:update", this.features_changed);
        this.editableFeatures.on("pm:dragend", this.features_changed);
        map.on("layeradd", this.features_changed);
      },
      addGeoJson(res_json) {
        new GeoJSON(res_json, {
          onEachFeature: (feature, layer) => {
            addPropertiesPopup(layer, feature);
            this.editableFeatures.addLayer(layer);
          },
        });
        let bounds = this.editableFeatures.getBounds();
        if (bounds.isValid()) {
          this.bigmap.fitBounds(bounds.pad(1.5));
        }
      },
      uploadFiles(event) {
        for (let file of event.target.files) {
          const reader = new FileReader();
          reader.addEventListener("load", (event) => {
            this.addGeoJson(JSON.parse(event.target.result));
          });
          reader.readAsText(file);
        }
        event.target.value = null;
      },
    },
  };
  function addPropertiesPopup(layer, feature) {
    let colormap = {
      contract_area: "yellow",
      intended_area: "orange",
      production_area: "red",
    };
    if (feature.geometry.type === "Point") return;
    let select = document.createElement("select"),
      option0 = document.createElement("option"),
      option1 = document.createElement("option"),
      option2 = document.createElement("option");

    select.addEventListener("change", function () {
      feature.properties.type = this.value;
      layer.setStyle({ color: colormap[this.value] });
    });
    option0.value = "contract_area";
    option0.innerHTML = "Contract area";
    option1.value = "intended_area";
    option1.innerHTML = "Intended area";
    option2.value = "production_area";
    option2.innerHTML = "Production area";
    select.appendChild(option0);
    select.appendChild(option1);
    select.appendChild(option2);
    select.value = feature.properties.type;

    layer.setStyle({ color: colormap[select.value] });
    layer.bindPopup(select);
  }
</script>

<style lang="scss" scoped></style>
