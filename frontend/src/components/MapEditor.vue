<template>
  <div class="container">
    <div class="locationlist">
      <div v-for="(loc, index) in deal.locations" :key="index" class="panel-body">
        <h3 @click="activeLocation = activeLocation !== loc ? loc : null">
          {{ $t("Location") }} <small>#{{ index + 1 }}</small>
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('removeEntry', index)"
          >
            <i class="fa fa-minus"></i>
          </button>
        </h3>
        <div v-if="activeLocation === loc">
          <EditField
            v-for="fieldname in fields"
            :key="fieldname"
            :fieldname="fieldname"
            v-model="loc[fieldname]"
            model="location"
            :label-classes="['col-12', 'small']"
            :value-classes="['col-12']"
          />
        </div>
      </div>
    </div>
    <div class="mapview">
      <BigMap
        :center="[12, 30]"
        :container-style="{ 'max-height': '600px', height: '600px' }"
        @ready="mapIsReady"
      />
      <form enctype="multipart/form-data" novalidate>
        Upload GeoJSON file
        <input type="file" multiple class="input-file" @change="uploadFiles" />
      </form>
      <ul class="small">
        <li v-for="feat in this.deal.geojson.features">
          {{ feat.geometry }} --- {{ feat.properties }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import BigMap from "$components/BigMap";
  import EditField from "$components/Fields/EditField";
  import "@geoman-io/leaflet-geoman-free";
  import { FeatureGroup, GeoJSON } from "leaflet";

  export default {
    components: { EditField, BigMap },
    props: {
      deal: { type: Object, required: true },
      fields: { type: Array, required: true },
    },
    data() {
      return {
        bigmap: null,
        editableFeatures: new FeatureGroup(),
        activeLocation: null,
      };
    },
    computed: {
      locationGoogleAutocomplete() {
        return this.$store.state.map.locationGoogleAutocomplete;
      },
    },
    watch: {
      activeLocation() {
        this.editableFeatures.eachLayer((l) => {
          let relevant_element = l?._icon || l._renderer._container;
          if (
            this.activeLocation?.id &&
            l.feature.properties.id !== this.activeLocation.id
          ) {
            relevant_element.classList.add("leaflet-hidden");
          } else {
            relevant_element.classList.remove("leaflet-hidden");
          }
        });
        // map.pm.controls
        //  control-icon leaflet-pm-icon-marker
      },
      locationGoogleAutocomplete() {
        let lGA = this.locationGoogleAutocomplete;
        this.editableFeatures.eachLayer((l) => {
          if (l?._icon && l.feature.properties.id === this.activeLocation.id) {
            l.setLatLng(lGA.latLng);

            if (!this.bigmap.getBounds().contains(lGA.latLng)) {
              if (lGA.viewport) {
                let vp_json = lGA.viewport.toJSON();
                this.bigmap.fitBounds([
                  [vp_json.south, vp_json.west],
                  [vp_json.north, vp_json.east],
                ]);
              } else {
                this.bigmap.setView(lGA.latLng);
              }
            }
          }
        });
        console.log(lGA);
      },
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

        map.on("pm:create", ({ layer, shape }) => {
          const leafId = layer._leaflet_id;
          const featureGroup = new FeatureGroup().addLayer(layer);
          this.editableFeatures.eachLayer((lay) => {
            if (lay._leaflet_id === leafId) this.editableFeatures.removeLayer(lay);
          });
          const data = featureGroup.toGeoJSON();
          data.features[0].properties = {
            id: this.activeLocation?.id,
            name: this.activeLocation.name,
          };
          this.addGeoJson(data);

          this.features_changed();
        });
        map.on("pm:remove", this.features_changed);
        this.editableFeatures.on("pm:update", this.features_changed);
        this.editableFeatures.on("pm:dragend", this.features_changed);
        map.on("layeradd", this.features_changed);
      },
      addGeoJson(res_json) {
        new GeoJSON(res_json, {
          onEachFeature: (feature, layer) => {
            if (feature.geometry.type === "Point") {
              layer.addEventListener("click", () => {
                let loc = this.deal.locations.filter(
                  (l) => l.id === feature.properties.id
                )[0];
                this.activeLocation = this.activeLocation !== loc ? loc : null;
              });
            } else {
              this.addPropertiesPopup(layer, feature);
            }
            this.editableFeatures.addLayer(layer);
          },
        });

        let bounds = this.editableFeatures.getBounds();
        if (bounds.isValid()) this.bigmap.fitBounds(bounds.pad(1.5));
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
      addPropertiesPopup(layer, feature) {
        let colormap = {
          contract_area: "yellow",
          intended_area: "orange",
          production_area: "red",
        };

        let select = document.createElement("select"),
          option0 = document.createElement("option"),
          option1 = document.createElement("option"),
          option2 = document.createElement("option");

        select.addEventListener("change", ({ target }) => {
          feature.properties.type = target.value;
          layer.setStyle({ color: colormap[target.value] });
          this.features_changed();
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
      },
    },
  };
</script>

<style lang="scss" scoped>
  .container {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
  }
  .locationlist {
    padding-right: 1em;
    grid-column: span 4;
  }
  .mapview {
    grid-column: span 8;
  }
</style>

<style>
  svg.leaflet-hidden {
    display: none;
    /*opacity: 0.15;*/
  }
  img.leaflet-hidden {
    /*display: none;*/
    opacity: 0.15;
  }
</style>
