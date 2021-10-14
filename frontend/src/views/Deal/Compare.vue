<template>
  <div class="container deal-detail">
    <div v-if="dealdiff" class="row">
      <div class="col-sm-5 col-md-3">
        <h1>Deal #{{ dealId }}</h1>
      </div>
      <div class="col-sm-7 col-md-9 panel-container"></div>
      <div class="col">
        <h3 class="my-2">Comparing versions {{ fromVersion }} and {{ toVersion }}</h3>
      </div>
    </div>

    <table class="table table-striped">
      <thead>
        <tr>
          <th class="col-2"></th>
          <th class="col-5">{{ fromVersion }}</th>
          <th class="col-5">{{ toVersion }}</th>
        </tr>
      </thead>

      <tbody>
        <template v-for="section in deal_sections" v-if="anyFieldFromSection(section)">
          <tr>
            <th colspan="3">
              <h2>{{ section.label }}</h2>
            </th>
          </tr>
          <template
            v-for="subsec in section.subsections"
            v-if="anyFieldFromSubSection(subsec)"
          >
            <tr>
              <th colspan="3">
                <h3>{{ subsec.name }}</h3>
              </th>
            </tr>
            <tr v-for="field in subsec.fields" v-if="dealdiff.has(field)">
              <th class="col-2">
                <FieldLabel :fieldname="field" :label-classes="[]" />
              </th>
              <td class="col-5">
                <DisplayField
                  :fieldname="field"
                  :show-label="false"
                  :value="from_deal[field]"
                />
              </td>
              <td class="col-5">
                <DisplayField
                  :fieldname="field"
                  :show-label="false"
                  :value="to_deal[field]"
                />
              </td>
            </tr>
          </template>
        </template>

        <template v-if="locationsdiff">
          <tr>
            <th colspan="3">
              <h2>{{ $t("Locations") }}</h2>
            </th>
          </tr>
          <template v-for="field in locationsdiff">
            <tr>
              <th colspan="3">
                <h3>{{ $t("Location") }} #{{ +field + 1 }}</h3>
              </th>
            </tr>
            <tr v-for="jfield in deal_submodel_sections.location">
              <th class="col-2">
                <FieldLabel :fieldname="jfield" :label-classes="[]" model="location" />
              </th>
              <td class="col-5">
                <DisplayField
                  v-if="from_deal.locations[field]"
                  :fieldname="jfield"
                  :show-label="false"
                  :value="from_deal.locations[field][jfield]"
                  model="location"
                />
              </td>
              <td class="col-5">
                <DisplayField
                  v-if="to_deal.locations[field]"
                  :fieldname="jfield"
                  :show-label="false"
                  :value="to_deal.locations[field][jfield]"
                  model="location"
                />
              </td>
            </tr>
          </template>
        </template>

        <template v-if="datasourcesdiff">
          <tr>
            <th colspan="3">
              <h2>{{ $t("Data sources") }}</h2>
            </th>
          </tr>
          <template v-for="field in datasourcesdiff">
            <tr>
              <th colspan="3">
                <h3>{{ $t("Data source") }} #{{ +field + 1 }}</h3>
              </th>
            </tr>
            <tr v-for="jfield in deal_submodel_sections.datasource">
              <th class="col-2">
                <FieldLabel
                  :fieldname="jfield"
                  :label-classes="[]"
                  model="datasource"
                />
              </th>
              <td class="col-5">
                <DisplayField
                  v-if="from_deal.datasources[field]"
                  :fieldname="jfield"
                  :show-label="false"
                  :value="from_deal.datasources[field][jfield]"
                  model="datasource"
                />
              </td>
              <td class="col-5">
                <DisplayField
                  v-if="to_deal.datasources[field]"
                  :fieldname="jfield"
                  :show-label="false"
                  :value="to_deal.datasources[field][jfield]"
                  model="datasource"
                />
              </td>
            </tr>
          </template>
        </template>

        <template v-if="contractsdiff">
          <tr>
            <th colspan="3">
              <h2>{{ $t("Contracts") }}</h2>
            </th>
          </tr>
          <template v-for="field in contractsdiff">
            <tr>
              <th colspan="3">
                <h3>{{ $t("Contract") }} #{{ +field + 1 }}</h3>
              </th>
            </tr>
            <tr v-for="jfield in deal_submodel_sections.contract">
              <th class="col-2">
                <FieldLabel :fieldname="jfield" :label-classes="[]" model="contract" />
              </th>
              <td class="col-5">
                <DisplayField
                  v-if="from_deal.contracts[field]"
                  :fieldname="jfield"
                  :show-label="false"
                  :value="from_deal.contracts[field][jfield]"
                  model="contract"
                />
              </td>
              <td class="col-5">
                <DisplayField
                  v-if="to_deal.contracts[field]"
                  :fieldname="jfield"
                  :show-label="false"
                  :value="to_deal.contracts[field][jfield]"
                  model="contract"
                />
              </td>
            </tr>
          </template>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
  import DisplayField from "$components/Fields/DisplayField";
  import FieldLabel from "$components/Fields/FieldLabel";
  import { deal_gql_query } from "$store/queries";

  import { diff } from "deep-object-diff";

  import { deal_sections, deal_submodel_sections } from "./deal_sections";
  import Vue from "vue";

  export default Vue.extend({
    name: "Compare",
    components: {
      FieldLabel,
      DisplayField,
    },
    props: {
      dealId: { type: [Number, String], required: true },
      fromVersion: { type: [Number, String], default: null },
      toVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        from_deal: null,
        to_deal: null,
        loading: false,
        deal_sections,
        deal_submodel_sections,
        investor: { involvements: [] },
        dodiff: diff,
      };
    },
    computed: {
      dealdiff() {
        let diffy = diff(this.from_deal, this.to_deal);
        if (diffy) return new Set(Object.keys(diffy));
        return new Set();
      },
      locationsdiff() {
        if (!this.from_deal || !this.to_deal) return;
        let diffy = diff(this.from_deal.locations, this.to_deal.locations);
        if (diffy && Object.keys(diffy).length) return new Set(Object.keys(diffy));
      },
      datasourcesdiff() {
        if (!this.from_deal || !this.to_deal) return;
        let diffy = diff(this.from_deal.datasources, this.to_deal.datasources);
        if (diffy && Object.keys(diffy).length > 0) return new Set(Object.keys(diffy));
      },
      contractsdiff() {
        if (!this.from_deal || !this.to_deal) return;
        let diffy = diff(this.from_deal.contracts, this.to_deal.contracts);
        if (diffy && Object.keys(diffy).length > 0) return new Set(Object.keys(diffy));
      },
    },
    created() {
      this.$apollo
        .query({
          query: deal_gql_query,
          variables: {
            id: +this.dealId,
            version: +this.fromVersion,
            subset: this.$store.state.page.user ? "UNFILTERED" : "PUBLIC",
          },
        })
        .then((data) => (this.from_deal = data.data.deal));
      this.$apollo
        .query({
          query: deal_gql_query,
          variables: {
            id: +this.dealId,
            version: +this.toVersion,
            subset: this.$store.state.page.user ? "UNFILTERED" : "PUBLIC",
          },
        })
        .then((data) => (this.to_deal = data.data.deal));
    },
    methods: {
      anyFieldFromSection(section) {
        return section.subsections.some((subsec) =>
          this.anyFieldFromSubSection(subsec)
        );
      },
      anyFieldFromSubSection(subsec) {
        return subsec.fields.some((f) => this.dealdiff.has(f));
      },
    },
  });
</script>

<style scoped>
  tr {
    display: -ms-flexbox !important;
    display: flex !important;
  }
</style>
