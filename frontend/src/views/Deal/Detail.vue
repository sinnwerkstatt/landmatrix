<template>
  <div class="container" v-if="deal && deal_fields">
    <b-tabs
      content-class="mt-3"
      vertical
      pills
      nav-wrapper-class="position-relative"
      nav-class="sticky-nav"
    >

      <DealLocationSection
        :title="deal_fields.location.label"
        :deal="deal"
        :fields="deal_fields.location.fields"
        :readonly="true"
      />

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
  import store from "/store";
  import DealSection from "/components/Deal/DealSection";
  import DealLocationSection from "/components/Deal/DealLocationSection";

  import { mapState } from "vuex";
  import router from "/router";


  export default {
    props: ["deal_id"],
    components: { DealSection, DealLocationSection },
    data() {
      return {
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
    },
    beforeRouteEnter(to, from, next) {
      let title = `Deal #${to.params.deal_id}`;
      store
        .dispatch("setCurrentDeal", to.params.deal_id)
        .then(() => {
          store.dispatch("setPageContext", {
            title: title,
            breadcrumbs: [
              { link: { name: "wagtail" }, name: "Home" },
              { link: { name: "deal_list" }, name: "Data" },
              { name: title },
            ],
          });
          next();
        })
        .catch(() => {
          router.replace({ name: "404" });
        });
    },
  };
</script>

<style lang="scss">
  .sticky-nav {
    position: -webkit-sticky;
    position: sticky;
    top: 10%;
    z-index: 99;
  }
</style>
