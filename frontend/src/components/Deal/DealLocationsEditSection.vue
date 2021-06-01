<template>
  <div class="container">
    <div class="locationlist">
      <div v-for="(loc, index) in deal.locations" :key="index" class="panel-body">
        <h3
          :class="{ highlighted: hoverLocID === loc.id }"
          @click="activeLocation = activeLocation !== loc ? loc : null"
          @mouseover="hoverLocID = loc.id"
          @mouseout="hoverLocID = null"
        >
          {{ $t("Location") }} <small>#{{ loc.id }}</small>
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('removeEntry', index)"
          >
            <i class="fa fa-minus"></i>
          </button>
        </h3>
        <div v-if="activeLocation === loc">
          <div class="form-field row">
            <div class="col-12 small">
              {{ $t("Location") }}
            </div>
            <div class="col-12">
              <LocationGoogleField
                v-model="loc.name"
                :country-code="deal.country.code_alpha2"
                @change="locationGoogleAutocomplete"
              />
            </div>
          </div>

          <div class="form-field row">
            <div class="col-12 small">
              {{ $t("Point") }}
            </div>
            <div class="col-12">
              <PointField v-model="loc.point" @input="pointChange" />
            </div>
          </div>
          <div v-for="fieldname in fields" :key="fieldname">
            <EditField
              v-model="loc[fieldname]"
              :fieldname="fieldname"
              model="location"
              :label-classes="['col-12', 'small']"
              :value-classes="['col-12']"
            />
          </div>
        </div>
      </div>
      <button type="button" class="btn btn-primary" @click="addLocation">
        <i class="fa fa-plus"></i> {{ $t("Location") }}
      </button>
    </div>
    <div class="mapview">
      <BigMap
        :center="[12, 30]"
        :container-style="{ 'max-height': '65vh', height: '65vh' }"
        @ready="mapIsReady"
      />
      <form enctype="multipart/form-data" novalidate class="mt-3">
        Upload GeoJSON file
        <input type="file" multiple class="input-file" @change="uploadFiles" />
      </form>
    </div>
  </div>
</template>

<script>
  import BigMap from "$components/BigMap";
  import LocationGoogleField from "$components/Fields/Edit/LocationGoogleField";
  import PointField from "$components/Fields/Edit/PointField";
  import EditField from "$components/Fields/EditField";
  import "@geoman-io/leaflet-geoman-free";
  import { GeoJSON, LatLngBounds, Marker } from "leaflet";

  export default {
    components: { PointField, LocationGoogleField, EditField, BigMap },
    props: {
      deal: { type: Object, required: true },
    },
    data() {
      return {
        fields: ["level_of_accuracy", "description", "facility_name", "comment"],
        bigmap: null,
        activeLocation: null,
        hoverLocID: null,
        locationFGs: new Map(),
        currentFG: null,
        geoman_opts: {
          position: "topleft",
          drawCircle: false,
          drawCircleMarker: false,
          drawRectangle: false,
          drawPolyline: false,
          cutPolygon: false,
          removalMode: false,
          drawMarker: false,
        },
        geojson_options: {
          onEachFeature: (feature, layer) => {
            // highlight location in list on map-hover
            layer.addEventListener(
              "mouseover",
              () => (this.hoverLocID = feature.properties.id)
            );
            layer.addEventListener("mouseout", () => (this.hoverLocID = null));

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
          },
        },
      };
    },
    computed: {
      // locationFGs() {
      //   let ret = {};
      //   if (!this.bigmap) return ret;
      //   this.deal.locations.forEach((loc) => {
      //     let fg = new FeatureGroup();
      //     ret[loc.id] = fg;
      //     this.addGeoJson(loc.areas, fg);
      //     this.bigmap.addLayer(fg);
      //     // console.log(loc.point);
      //     // console.log(loc.areas);
      //   });
      //   return ret;
      // },
    },
    watch: {
      "deal.country"(nCa) {
        this.bigmap.fitBounds([
          [nCa.point_lat_min, nCa.point_lon_min],
          [nCa.point_lat_max, nCa.point_lon_max],
        ]);
      },
      // currentFG() {
      //   this.bigmap.pm.setGlobalOptions({ layerGroup: this.currentFG });
      // },
      activeLocation(actLoc) {
        let drawMarker = true;
        if (actLoc) {
          if (!this.locationFGs.get(actLoc.id)) {
            let fg = new GeoJSON(null, this.geojson_options);
            fg.on("pm:update", this.features_changed);
            this.locationFGs.set(actLoc.id, fg);
            this.bigmap.addLayer(fg);
          }
          this.currentFG = this.locationFGs.get(actLoc.id);

          this.currentFG.eachLayer((l) => {
            if (l.feature.geometry.type === "Point") {
              drawMarker = false;
            }
          });

          this.bigmap.pm.setGlobalOptions({ layerGroup: this.currentFG });
          this.bigmap.pm.addControls({
            ...this.geoman_opts,
            drawMarker,
          });
        } else {
          this.bigmap.pm.removeControls();
        }

        // this.editableFeatures.eachLayer((l) => {
        //   let relevant_element = l?._icon || l._renderer._container;
        //   if (actLoc && l.feature.properties.id !== this.activeLocation.id) {
        //     relevant_element.classList.add("leaflet-hidden");
        //   } else {
        //     if (l.feature.geometry.type === "Point") {
        //       drawMarker = false;
        //     }
        //     relevant_element.classList.remove("leaflet-hidden");
        //   }
        // });
      },
      hoverLocID() {
        // this.editableFeatures.onEachFeature((l) => {
        //   let relevant_element = l?._icon || l._renderer._container;
        //   if (this.hoverLocID && l.feature.properties.id !== this.hoverLocID) {
        //     relevant_element.classList.add("leaflet-unhighlight");
        //   } else {
        //     relevant_element.classList.remove("leaflet-unhighlight");
        //   }
        // });
        // map.pm.controls
        //  control-icon leaflet-pm-icon-marker
      },
    },
    methods: {
      addLocation() {
        let maxid = 0;
        this.deal.locations.forEach((l) => (maxid = Math.max(l.id, maxid)));
        let newloc = new Object({ id: maxid + 1 });
        this.deal.locations.push(newloc);
        this.activeLocation = newloc;
      },
      pointChange(lPo) {
        // console.log({ lPo });
        // this.editableFeatures.eachLayer((l) => {
        //   if (l?._icon && l.feature.properties.id === this.activeLocation.id) {
        //     l.setLatLng(lPo);
        //     this.bigmap.setView(lPo);
        //     // alternative approach to focussing
        //     // this.bigmap.fitBounds(this.editableFeatures.getBounds().pad(0.2));
        //   }
        // });
      },
      locationGoogleAutocomplete(lGA) {
        let hasMarker = false;
        this.currentFG.eachLayer((l) => {
          if (l?._icon && l.feature.properties.id === this.activeLocation.id) {
            hasMarker = true;
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
        if (!hasMarker) {
          let lpoint = new Marker(lGA.latLng).toGeoJSON();
          lpoint.properties = {
            id: this.activeLocation?.id,
            name: this.activeLocation.name,
          };
          this.currentFG.addData(lpoint);
        }
      },
      features_changed() {
        let newlocs = [];
        this.deal.locations.forEach((l) => {
          let lfg = this.locationFGs.get(l.id);
          if (lfg) {
            let lfggeo = lfg.toGeoJSON();
            l.areas = lfggeo;
            let lpoint = lfggeo.features.find((f) => f.geometry.type === "Point");
            if (lpoint) {
              const [lng, lat] = lpoint.geometry.coordinates;
              l.point = { lat, lng };
            }
          }
          newlocs.push(l);
        });
        this.deal.locations = newlocs;
        // this.editableFeatures.eachLayer((l) => {
        //   let locJson = l.toGeoJSON();
        //   // if (layer.feature.geometry.type ==='Point') {
        //   if (locJson.geometry.type === "Point") {
        //     console.log({ oldP: this.activeLocation.point, newP: l.getLatLng() });
        //     this.activeLocation.point = l.getLatLng();
        //   }
        //
        //   console.log({ locJson });
        //   console.log(deal_location_map[locJson.properties.id].areas);
        // });
        // let loc = this.activeLocation;
        // console.log(loc);
      },
      mapIsReady(map) {
        this.bigmap = map;

        let bounds = new LatLngBounds([]);
        this.deal.locations.forEach((loc) => {
          let fg = new GeoJSON(null, this.geojson_options);
          fg.on("pm:update", this.features_changed);
          this.locationFGs[loc.id] = fg;
          this.bigmap.addLayer(fg);

          if (loc.areas) fg.addData(loc.areas);

          if (loc.point) {
            let pt = new Marker(loc.point).toGeoJSON();
            pt.properties = { id: loc.id }; //, name: loc.name, type: "point" };
            fg.addData(pt);
          }
          bounds.extend(fg.getBounds());
        });

        if (!bounds.isValid()) {
          bounds = [
            [this.deal.country.point_lat_min, this.deal.country.point_lon_min],
            [this.deal.country.point_lat_max, this.deal.country.point_lon_max],
          ];
        }
        this.bigmap.fitBounds(bounds);

        map.on("pm:create", ({ layer, shape }) => {
          // do a little three-card monte carlo:
          // save the current id, remove it from existing layers and add it
          // back in geojson style after giving it props. 🙄
          const leafId = layer._leaflet_id;
          let tmpfg = new GeoJSON().addLayer(layer);
          this.currentFG.eachLayer((lay) => {
            if (lay._leaflet_id === leafId) this.currentFG.removeLayer(lay);
          });
          const data = tmpfg.toGeoJSON();
          data.features[0].properties = {
            id: this.activeLocation?.id,
            name: this.activeLocation.name,
          };
          this.currentFG.addData(data);

          this.bigmap.pm.disableDraw();
          this.bigmap.pm.removeControls();
          this.bigmap.pm.addControls(this.geoman_opts);

          this.features_changed();
        });

        // map.on("pm:remove", this.features_changed);
        // this.editableFeatures.on("pm:dragend", ({ layer }) => {
        //   this.features_changed();
        // });
        // map.on("layeradd", this.features_changed);
      },
      uploadFiles(event) {
        // for (let file of event.target.files) {
        //   const reader = new FileReader();
        //   reader.addEventListener("load", (event) => {
        //     this.addGeoJson(JSON.parse(event.target.result));
        //   });
        //   reader.readAsText(file);
        // }
        // event.target.value = null;
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
  @import "../../scss/colors";

  h3.highlighted {
    color: $lm_orange;
    //color: var(--color-lm-orange);
  }

  .container {
    padding-left: 0;
    padding-right: 0;
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
</style>
