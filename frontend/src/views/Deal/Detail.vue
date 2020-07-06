<template>
  <div class="container" v-if="deal && deal_fields">
    <b-tabs
      content-class="mt-3"
      vertical
      pills
      nav-wrapper-class="position-relative"
      nav-class="sticky-nav"
    >
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

      <DealSection
        :title="deal_fields.general_info.label"
        :deal="deal"
        :sections="deal_fields.general_info.subsections"
        :readonly="true"
      />

      <b-tab title="Contracts" v-if="deal.contracts.length">
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

      <DealSection
        :title="deal_fields.employment.label"
        :deal="deal"
        :sections="deal_fields.employment.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.investor_info.label"
        :deal="deal"
        :sections="deal_fields.investor_info.subsections"
        :readonly="true"
      />

      <b-tab title="Data sources" v-if="deal.datasources.length">
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

      <DealSection
        :title="deal_fields.local_communities.label"
        :deal="deal"
        :sections="deal_fields.local_communities.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.former_use.label"
        :deal="deal"
        :sections="deal_fields.former_use.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.produce_info.label"
        :deal="deal"
        :sections="deal_fields.produce_info.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.water.label"
        :deal="deal"
        :sections="deal_fields.water.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.gender_related_info.label"
        :deal="deal"
        :sections="deal_fields.gender_related_info.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.guidelines_and_principles.label"
        :deal="deal"
        :sections="deal_fields.guidelines_and_principles.subsections"
        :readonly="true"
      />
    </b-tabs>
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";

  import { LGeoJson } from "vue2-leaflet";
  import DealSection from "@/components/Deal/DealSection";
  import { mapState } from "vuex";

  export default {
    props: ["deal_id"],
    components: { DealSection, BigMap, LGeoJson },
    data() {
      return {
        location_fields: {
          name: "Name",
          description: "Description",
          // point: "Point",
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
      ...mapState({
        deal_fields: (state) => state.deal.deal_fields,
      }),
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

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }

  .sticky-nav {
    position: -webkit-sticky;
    position: sticky;
    top: 10%;
    z-index: 99;
  }
</style>
