<template>
  <div class="container">
    <div class="locationlist">
      <div v-for="(loc, index) in locs" :key="index" class="panel-body">
        <div class="location-header">
          <i
            class="expand-toggle fas fa-chevron-down"
            :class="{
              'fa-chevron-up': actLoc === loc,
              'fa-chevron-down': actLoc !== loc,
            }"
            @click="actLoc = actLoc !== loc ? loc : null"
          ></i>
          <h3
            :class="{ highlighted: hoverLocID === loc.id }"
            @click="actLoc = actLoc !== loc ? loc : null"
            @mouseover="hoverLocID = loc.id"
            @mouseout="hoverLocID = null"
          >
            {{ index + 1 }}. {{ $t("Location") }}
            <small class="font-mono">({{ loc.id }})</small>
          </h3>
          <a class="trashbin" @click="removeLocation(loc.id)">
            <i class="fas fa-trash"></i>
          </a>
        </div>
        <div :class="{ hidden: actLoc !== loc }" class="location-body">
          <EditField
            v-model="loc.level_of_accuracy"
            fieldname="level_of_accuracy"
            model="location"
            :label-classes="['col-12', 'mb-2']"
            :value-classes="['col-12', 'mb-1']"
            @input="_features_changed"
          />
          <div class="form-field row">
            <div class="col-12 mb-2">
              {{ $t("Location") }}
            </div>
            <div class="col-12 mb-3">
              <LocationGoogleField
                v-model="loc.name"
                :country-code="country.code_alpha2"
                @change="locationGoogleAutocomplete"
              />
            </div>
          </div>

          <div class="form-field row">
            <div class="col-12 mb-1">
              {{ $t("Point") }}
            </div>
            <div class="col-12 mb-3">
              <PointField :value="loc.point" @input="pointChange" />
            </div>
          </div>
          <div v-for="fieldname in fields" :key="fieldname">
            <EditField
              v-model="loc[fieldname]"
              :fieldname="fieldname"
              model="location"
              :label-classes="['col-12', 'mb-2']"
              :value-classes="['col-12', 'mb-3']"
              @input="_features_changed"
            />
          </div>
          <div class="row">
            <form enctype="multipart/form-data" novalidate class="mt-3">
              <div class="col-12 mb-1">{{ $t("Add intended area (as GeoJSON)") }}</div>
              <div class="col-12 mb-2">
                <input
                  type="file"
                  class="input-file"
                  accept=".geojson,application/geo+json,application/json"
                  @change="uploadFiles('intended_area', $event)"
                />
              </div>
              <div class="col-12 mb-1">{{ $t("Add contract area (as GeoJSON)") }}</div>
              <div class="col-12 mb-2">
                <input
                  type="file"
                  class="input-file"
                  accept=".geojson,application/geo+json,application/json"
                  @change="uploadFiles('contract_area', $event)"
                />
              </div>
              <div class="col-12 mb-1">
                {{ $t("Add production area (as GeoJSON)") }}
              </div>
              <div class="col-12 mb-2">
                <input
                  type="file"
                  class="input-file"
                  accept=".geojson,application/geo+json,application/json"
                  @change="uploadFiles('production_area', $event)"
                />
              </div>
            </form>
          </div>
        </div>
      </div>
      <button type="button" class="btn btn-secondary mt-3" @click="addLocation">
        <i class="fa fa-plus"></i> {{ $t("Add location") }}
      </button>
    </div>
    <div class="mapview">
      <BigMap
        :center="[12, 30]"
        :container-style="{ 'max-height': '65vh', height: '65vh' }"
        @ready="mapIsReady"
      />
    </div>
  </div>
</template>

<script lang="ts">
  import BigMap from "$components/BigMap.vue";
  import LocationGoogleField from "$components/Fields/Edit/LocationGoogleField.vue";
  import PointField from "$components/Fields/Edit/PointField.vue";
  import EditField from "$components/Fields/EditField.vue";
  import type { Location } from "$types/deal";
  import type { Country } from "$types/wagtail";
  import { newNanoid } from "$utils";
  import "@geoman-io/leaflet-geoman-free";
  import type { Feature, GeoJsonObject } from "geojson";
  import type L from "leaflet";
  import { GeoJSON, LatLngBounds, Marker } from "leaflet";
  import Vue from "vue";
  import type { PropType } from "vue";

  export default Vue.extend({
    components: { PointField, LocationGoogleField, EditField, BigMap },
    props: {
      locations: { type: Array as PropType<Location[]>, required: true },
      country: { type: Object as PropType<Country>, required: true },
    },
    data() {
      return {
        fields: ["description", "facility_name", "comment"],
        bigmap: null as unknown as L.Map,
        locs: [] as Location[],
        actLoc: null as Location | null,
        hoverLocID: null as number | null,
        locationFGs: new Map() as Map<number, L.GeoJSON>,
        actFG: undefined as L.GeoJSON | undefined,
        geoman_opts: {
          position: "topleft" as L.ControlPosition,
          drawCircle: false,
          drawCircleMarker: false,
          drawRectangle: false,
          drawPolyline: false,
          drawPolygon: false,
          cutPolygon: false,
          drawMarker: false,
        },
      };
    },
    computed: {
      geojson_options() {
        return {
          onEachFeature: (feature: Feature, layer: L.Layer) => {
            // highlight location in list on map-hover
            layer.addEventListener(
              "mouseover",
              () => (this.hoverLocID = feature.properties?.id)
            );
            layer.addEventListener("mouseout", () => (this.hoverLocID = null));

            if (feature.geometry.type === "Point") {
              layer.addEventListener("click", () => {
                this.actLoc = this.locs.filter(
                  (l) => l.id === feature.properties?.id
                )[0];
              });
            } else {
              this._addPropertiesPopup(layer, feature);
            }
          },
        };
      },
    },
    watch: {
      country(nCa) {
        this.bigmap.fitBounds([
          [nCa.point_lat_min, nCa.point_lon_min],
          [nCa.point_lat_max, nCa.point_lon_max],
        ]);
      },
      actLoc(actLoc) {
        let drawMarker = true;
        if (actLoc) {
          if (!this.locationFGs.get(actLoc.id)) this._addNewLayerGroup(actLoc.id);
          this.actFG = this.locationFGs.get(actLoc.id);
          this.actFG?.eachLayer((l) => {
            if (l.feature.geometry.type === "Point") drawMarker = false;
          });
          // noinspection JSCheckFunctionSignatures,TypeScriptValidateJSTypes
          this.bigmap.pm.setGlobalOptions({ layerGroup: this.actFG });
          this.bigmap.pm.addControls({ ...this.geoman_opts, drawMarker });
        } else {
          this.bigmap.pm.removeControls();
        }
        this.locationFGs.forEach((value, key) => {
          value.eachLayer((l: L.Layer) => {
            let relevant_element = l?._icon || l._path;
            if (actLoc && key !== actLoc.id)
              relevant_element.classList.add("leaflet-hidden");
            else relevant_element.classList.remove("leaflet-hidden");
          });
        });
      },
      hoverLocID() {
        this.locationFGs.forEach((value, key) => {
          value.eachLayer((l: L.Layer) => {
            let relevant_element = l?._icon || l._path;
            if (this.hoverLocID && key !== this.hoverLocID)
              relevant_element.classList.add("leaflet-unhighlight");
            else relevant_element.classList.remove("leaflet-unhighlight");
          });
        });
      },
    },
    created() {
      this.locs = JSON.parse(JSON.stringify(this.locations));
    },
    methods: {
      mapIsReady(map: L.Map) {
        this.bigmap = map;

        this.locs.forEach((loc) => {
          let fg = this._addNewLayerGroup(loc.id);
          if (loc.areas) fg.addData(loc.areas);
          if (loc.point) {
            let pt = new Marker(loc.point).toGeoJSON();
            pt.properties = { id: loc.id }; //, name: loc.name, type: "point" };
            fg.addData(pt);
          }
        });
        this._fit_bounds();
        this.bigmap.on("pm:remove", this._features_changed);
        this.bigmap.on("pm:create", this._on_pm_create);
        if (this.locs.length === 1) this.actLoc = this.locs[0];
      },
      addLocation() {
        const currentIDs = this.locs.map((x) => `${x.id}`);
        let newloc = new Object({ id: newNanoid(currentIDs) }) as Location;
        this.actLoc = newloc;
        this.locs.push(newloc);
        this._features_changed();
      },
      removeLocation(id: string) {
        let message = `${this.$t("Remove")} ${this.$t("location")} ${id}?`;
        this.$bvModal;
        this.$bvModal
          .msgBoxConfirm(message, {
            size: "sm",
            okTitle: this.$t("Delete").toString(),
            cancelTitle: this.$t("Cancel").toString(),
            centered: true,
          })
          .then((confirmed) => {
            if (confirmed) {
              let idx = this.locs.findIndex((x) => x.id === id);
              let loc = this.locs.splice(idx, 1)[0];
              let fg = this.locationFGs.get(loc.id);
              this.locationFGs.delete(loc.id);
              this.bigmap.removeLayer(fg);
              this._features_changed();
            }
          });
      },
      locationGoogleAutocomplete(lGA: { latLng: [number, number] }) {
        let hasMarker = false;
        this.actFG?.eachLayer((l: L.Layer) => {
          if (l?._icon && l.feature.properties.id === this.actLoc?.id) {
            hasMarker = true;
            (l as L.Marker).setLatLng(lGA.latLng);
          }
        });
        if (!hasMarker) {
          let lpoint = new Marker(lGA.latLng).toGeoJSON();
          lpoint.properties = { id: this.actLoc?.id, name: this.actLoc?.name };
          this.actFG?.addData(lpoint);
        }
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
        this._features_changed();
      },
      pointChange(lPo: { lat: number; lng: number }) {
        let hasMarker = false;
        this.actFG?.eachLayer((l) => {
          if (l?._icon && l.feature.properties.id === this.actLoc?.id) {
            hasMarker = true;
            (l as L.Marker).setLatLng(lPo);
            // this.bigmap.setView(lPo);
            // alternative approach to focussing
            // this.bigmap.fitBounds(this.editableFeatures.getBounds().pad(0.2));
          }
        });
        if (!hasMarker) {
          if (!lPo.lat || !lPo.lng) return;
          let lpoint = new Marker(lPo).toGeoJSON();
          lpoint.properties = { id: this.actLoc?.id, name: this.actLoc?.name };
          this.actFG?.addData(lpoint);
        }
        this._features_changed();
      },
      uploadFiles(area_type: string, event: Event) {
        const target = event.target as HTMLInputElement;
        if (!target || !target.files || target.files.length <= 0) return;

        const reader = new FileReader();
        reader.addEventListener("load", (event) => {
          if (!this.actFG) return;
          let result = JSON.parse(event.target?.result as string);
          const features: Feature[] = result.features.map((f: Feature) => {
            if (f.properties) f.properties.type = area_type;
            else f.properties = { type: area_type };
            return f;
          });
          this.actFG.addData({ type: "FeatureCollection", features } as GeoJsonObject);
          let bounds = this.bigmap.getBounds();
          bounds.extend(this.actFG.getBounds());
          this.bigmap.fitBounds(bounds);
        });
        reader.readAsText(target?.files[0]);

        target.value = "";
      },
      _addNewLayerGroup(id: number) {
        let fg = new GeoJSON(undefined, this.geojson_options);
        fg.on("pm:update", this._features_changed);
        fg.on("pm:dragend", this._features_changed);
        fg.on("pm:rotateend", this._features_changed);
        this.locationFGs.set(id, fg);
        this.bigmap.addLayer(fg);
        return fg;
      },
      _addPropertiesPopup(layer, feature: Feature) {
        let colormap: { [key: string]: string } = {
          contract_area: "#ff00ff",
          intended_area: "#66ff33",
          production_area: "#ff0000",
          "": "#ffe600",
        };

        let select = document.createElement("select");
        [
          { value: "contract_area", innerHTML: this.$t("Contract area") },
          { value: "intended_area", innerHTML: this.$t("Intended area") },
          { value: "production_area", innerHTML: this.$t("Production area") },
        ].forEach((optn) => {
          let option = document.createElement("option");
          option.value = optn.value;
          option.innerHTML = optn.innerHTML.toString();
          select.appendChild(option);
        });
        select.addEventListener("change", (event) => {
          const target = event.target as HTMLSelectElement;
          if (target?.value) {
            if (feature.properties) feature.properties.type = target.value;
            else feature.properties = { type: target.value };
            layer.setStyle({ color: colormap[target.value] });
            this._features_changed();
          }
        });

        select.value = feature.properties?.type;
        layer.setStyle({ color: colormap[select.value] });
        layer.bindPopup(select);
      },
      _features_changed() {
        this.locs.forEach((l) => {
          let lfg = this.locationFGs.get(l.id);
          if (lfg && lfg.getLayers().length > 0) {
            let lfggeo = lfg.toGeoJSON();

            let pointIndex = lfggeo.features.findIndex(
              (f) => f.geometry.type === "Point"
            );
            if (pointIndex >= 0) {
              let lpoint = lfggeo.features.splice(pointIndex, 1);
              const [lng, lat] = lpoint[0].geometry.coordinates;
              l.point = { lat, lng };
            } else {
              l.point = {};
            }

            l.areas = lfggeo;
          }
        });
        this.$emit("input", this.locs);
        // this._fit_bounds();
      },
      _fit_bounds() {
        let bounds = new LatLngBounds([]);
        this.locationFGs.forEach((value) => {
          bounds.extend(value.getBounds());
        });
        if (bounds.isValid()) bounds = bounds.pad(0.5);
        else {
          bounds = [
            [this.country.point_lat_min, this.country.point_lon_min],
            [this.country.point_lat_max, this.country.point_lon_max],
          ];
        }
        this.bigmap.fitBounds(bounds);
      },
      _on_pm_create({ layer, shape }) {
        if (!this.actFG) return;
        ////// do a little three-card monte carlo:
        // save the current id, remove it from existing layers and add it
        // back in geojson style after giving it props. 🙄
        const leafId = layer._leaflet_id;
        const tmpfg = new GeoJSON().addLayer(layer).toGeoJSON();
        this.actFG.eachLayer((lay) => {
          if (lay._leaflet_id === leafId) this.actFG.removeLayer(lay);
        });

        let hasPoint = false;
        this.actFG.eachLayer((lay) => {
          if (lay.feature.geometry.type === "Point") hasPoint = true;
        });
        if (hasPoint) return;

        tmpfg.features[0].properties = {
          id: this.actLoc?.id,
          name: this.actLoc.name,
        };
        this.actFG.addData(tmpfg);
        ////// end of three-card monte carlo

        // reset Marker
        if (shape === "Marker") {
          let [lng, lat] = tmpfg.features[0].geometry.coordinates;
          this.actLoc.point = { lat, lng };

          this.bigmap.pm.disableDraw();
          this.bigmap.pm.removeControls();
          this.bigmap.pm.addControls(this.geoman_opts);
        }

        this._features_changed();
      },
    },
  });
</script>

<style lang="scss" scoped>
  h3.highlighted {
    color: var(--color-lm-orange);
    //color: var(--color-lm-orange);
  }

  .container {
    padding-left: 0;
    padding-right: 0;
    display: grid;
    grid-template-columns: repeat(12, 1fr);
  }

  .locationlist {
    grid-column: span 4;
    @media only screen and (max-width: 992px) {
      grid-column: span 12;
      order: 2;
    }
  }

  .mapview {
    grid-column: span 8;
    @media only screen and (max-width: 992px) {
      grid-column: span 12;
      order: 1;
      margin-bottom: 1rem;
    }
  }

  .location-header {
    display: flex;
    align-items: center;

    .expand-toggle {
      &:hover {
        cursor: pointer;
      }
    }

    h3 {
      margin: 0;

      &:hover {
        cursor: pointer;
      }
    }

    margin-bottom: 1em;

    & .expand-toggle {
      margin-right: 0.5em;
    }
  }

  .location-body {
    margin-bottom: 2em;
  }

  .fa-plus {
    margin-right: 0.3em;
  }

  .trashbin {
    margin-left: 2em;
    color: var(--color-lm-orange);

    &:hover {
      cursor: pointer;
      color: var(--color-lm-orange-light);
      text-decoration: none;
    }
  }

  input[type="file"] {
    width: 100%;
    min-width: 100%;
  }
</style>

<!--suppress CssUnusedSymbol -->
<style>
  .leaflet-unhighlight {
    opacity: 0.8;
    /*filter: grayscale(60%);*/
    filter: saturate(0.2);
  }

  svg.leaflet-hidden {
    display: none;
    /*opacity: 0.15;*/
  }

  img.leaflet-hidden {
    /*display: none;*/
    opacity: 0.6;
    filter: saturate(0);
    /*filter: grayscale(100%);*/
  }

  .locationlist .row {
    margin-left: 0;
    margin-right: 0;
  }
</style>
