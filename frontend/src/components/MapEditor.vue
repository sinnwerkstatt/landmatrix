<template>
  <div class="container">
    <big-map
      :containerStyle="{ 'max-height': '300px', height: '300px' }"
      @ready="pinTheMap"
    />
    <form enctype="multipart/form-data" novalidate>
      Upload GeoJSON file
      <input type="file" multiple @change="uploadFiles" class="input-file" />
    </form>
  </div>
</template>

<script>
  import "leaflet-draw";
  import BigMap from "/components/BigMap";

  function addPropertiesPopup(layer, feature) {
    let select = document.createElement("select"),
      option0 = document.createElement("option"),
      option1 = document.createElement("option"),
      option2 = document.createElement("option");

    select.addEventListener("change", function () {
      feature.properties.value = this.value;
      console.log(feature);
      let colormap = {
        contract_area: "yellow",
        intended_area: "orange",
        production_area: "red",
      };
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

    layer.bindPopup(select);
  }
  export default {
    components: {
      BigMap,
    },
    data() {
      return {
        bigmap: null,
        editableFeatures: new L.FeatureGroup(),
      };
    },
    methods: {
      pinTheMap(x) {
        this.bigmap = x;
        this.bigmap.addLayer(this.editableFeatures);

        this.bigmap.addControl(
          new L.Control.Draw({
            draw: {
              rectangle: false,
              circle: false,
              polyline: false,
              circlemarker: false,
            },
            edit: {
              featureGroup: this.editableFeatures,
            },
          })
        );

        this.bigmap.on(L.Draw.Event.CREATED, ({ layer }) =>
          this.editableFeatures.addLayer(layer)
        );
      },
      uploadFiles(event) {
        for (let file of event.target.files) {
          const reader = new FileReader();
          reader.addEventListener("load", (event) => {
            let res_json = JSON.parse(event.target.result);
            L.geoJSON(res_json, {
              onEachFeature: (feature, layer) => {
                addPropertiesPopup(layer, feature);
                this.editableFeatures.addLayer(layer);
              },
            });
          });
          reader.readAsText(file);
        }
        // TODO: Clear file selector afterwards.
        // event.target.value=null;
      },
    },
  };
</script>

<style lang="scss" scoped></style>
