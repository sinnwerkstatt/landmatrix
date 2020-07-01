<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mt-3" vertical pills>
      <b-tab title="Location" active>
        <div class="row">
          <div class="col">
            <div v-for="loc in deal.locations">
              <h3>Location #{{ loc.id }}</h3>
              <dl class="row">
                <template v-for="(name, field) in location_fields" v-if="loc[field]">
                  <dt class="col-3">{{ name }}</dt>
                  <dd class="col-9">{{ loc[field] }}</dd>
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

      <b-tab title="General Info">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>

      <b-tab title="Contracts">
        <div v-for="contract in deal.contracts">
          <h3>Contract #{{ contract.id }}</h3>
          <dl class="row">
            <template v-for="(name, field) in contract_fields" v-if="contract[field]">
              <dt class="col-3">{{ name }}</dt>
              <dd class="col-9">{{ contract[field] }}</dd>
            </template>
          </dl>
        </div>
      </b-tab>
      <b-tab title="Employment">
        <DealSection :deal="deal" :sections="employment" :readonly="true" />
      </b-tab>
      <b-tab title="Investor Info">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>
      <b-tab title="Data sources">
        <div v-for="datasource in deal.datasources">
          <h3>Data source #{{ datasource.id }}</h3>
          <dl class="row">
            <template
              v-for="(name, field) in datasource_fields"
              v-if="datasource[field]"
            >
              <dt class="col-3">{{ name }}</dt>
              <dd class="col-9">{{ datasource[field] }}</dd>
            </template>
          </dl>
        </div>
      </b-tab>
      <b-tab title="Local communities">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>
      <b-tab title="Former use">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>
      <b-tab title="Produce info">
        <DealSection :deal="deal" :sections="produce_info" :readonly="true" />
      </b-tab>
      <b-tab title="Water">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>
      <b-tab title="Gender-related info">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>
      <b-tab title="Guidelines & Principles">
        <DealSection :deal="deal" :sections="general_info" :readonly="true" />
      </b-tab>
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

  import { LGeoJson } from "vue2-leaflet";
  import { employment, general_info, produce_info } from "./deal_fields";
  import DealSection from "@/components/Deal/DealSection";

  export default {
    props: ["deal_id"],
    components: { DealSection, BigMap, LGeoJson },
    data() {
      return {
        general_info,
        employment,
        produce_info,
        location_fields: {
          name: "Name",
          description: "Description",
          point: "Point",
          facility_name: "Facility Name",
          level_of_accuracy: "Level of Accuracy",
          comment: "Comment",
        },
        datasource_fields: {
          type: "Type",
          url: "URL",
          file: "File",
          date: "Date",
          comment: "Comment",
        },
        contract_fields: {
          number: "Number",
          date: "Date",
          expiration_date: "Expiration Date",
          agreement_duration: "Duration of the agreement (in years)",
          comment: "Comment",
        },
      };
    },
    computed: {
      deal() {
        return this.$store.state.deal.current_deal;
      },
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
  };
</script>
