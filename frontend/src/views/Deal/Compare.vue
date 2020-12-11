<template>
  <div class="container deal-detail">
    <div class="loadingscreen" v-if="loading">
      <div class="loader"></div>
    </div>
    <div class="row" v-if="dealdiff">
      <div class="col-sm-5 col-md-3">
        <h1>Deal #{{ deal_id }}</h1>
      </div>
      <div class="col-sm-7 col-md-9 panel-container"></div>
      <div class="col">
        <h3 class="my-2">Comparing versions {{ from_version }} and {{ to_version }}</h3>
      </div>
    </div>

    <table class="table table-striped">
      <thead>
        <tr>
          <th></th>
          <th>{{ from_version }}</th>
          <th>{{ to_version }}</th>
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
              <th class="col-2"><FieldLabel :fieldname="field" /></th>
              <td class="col-5">
                <DisplayField
                  :show_label="false"
                  :fieldname="field"
                  :value="from_deal[field]"
                />
              </td>
              <td class="col-5">
                <DisplayField
                  :show_label="false"
                  :fieldname="field"
                  :value="to_deal[field]"
                />
              </td>
            </tr>
          </template>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
  import DealSection from "/components/Deal/DealSection";
  import DealHistory from "/components/Deal/DealHistory";
  import DealLocationsSection from "/components/Deal/DealLocationsSection";
  import DealSubmodelSection from "/components/Deal/DealSubmodelSection";
  import InvestorGraph from "/components/Investor/InvestorGraph";
  import { deal_sections, deal_submodel_sections } from "./deal_sections";
  import { deal_gql_query } from "/store/queries";
  import DealComments from "../../components/Deal/DealComments";
  import { diff } from "deep-object-diff";
  import { apolloClient } from "../../apolloclient";
  import DisplayField from "/components/Fields/DisplayField";
  import FieldLabel from "../../components/Fields/FieldLabel";

  export default {
    name: "Compare",
    props: ["deal_id", "deal_version", "from_version", "to_version"],
    components: {
      FieldLabel,
      DisplayField,
      DealComments,
      InvestorGraph,
      DealHistory,
      DealSection,
      DealLocationsSection,
      DealSubmodelSection,
    },
    data() {
      return {
        from_deal: null,
        to_deal: null,
        loading: false,
        deal_sections,
        deal_submodel_sections,
        investor: { involvements: [] },
      };
    },
    computed: {
      dealdiff() {
        let diffy = diff(this.from_deal, this.to_deal);
        if (diffy) return new Set(Object.keys(diffy));
        return new Set();
      },
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
    created() {
      apolloClient
        .query({
          query: deal_gql_query,
          variables: {
            id: +this.deal_id,
            version: +this.from_version,
            subset: this.$store.state.page.user ? "UNFILTERED" : "PUBLIC",
          },
        })
        .then((data) => (this.from_deal = data.data.deal));
      apolloClient
        .query({
          query: deal_gql_query,
          variables: {
            id: +this.deal_id,
            version: +this.to_version,
            subset: this.$store.state.page.user ? "UNFILTERED" : "PUBLIC",
          },
        })
        .then((data) => (this.to_deal = data.data.deal));
    },
  };
</script>
