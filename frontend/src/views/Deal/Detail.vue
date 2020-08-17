<template>
  <div class="container" v-if="deal">
    <div class="loadingscreen" v-if="loading">
      <div class="loader"></div>
    </div>
    <p v-if="not_public" class="alert alert-danger mb-4">{{ not_public }}</p>
    <!--    <div class="quicknav">-->
    <!--      <div v-for="(version, i) in deal.versions">-->
    <!--        <span v-if="(!deal_version && !i) || +deal_version === +version.revision.id"-->
    <!--          >Current</span-->
    <!--        >-->
    <!--        <router-link-->
    <!--          v-else-->
    <!--          :to="{-->
    <!--            name: 'deal_detail',-->
    <!--            params: { deal_id, deal_version: version.revision.id },-->
    <!--          }"-->
    <!--          >{{ version.revision.date_created | defaultdate }}</router-link-->
    <!--        >-->
    <!--      </div>-->
    <!--    </div>-->
    <b-tabs
      content-class="mt-3"
      vertical
      pills
      nav-wrapper-class="position-relative"
      nav-class="sticky-nav"
      :key="deal_id + deal_version"
    >
      <DealLocationSection
        :title="`Locations`"
        :deal="deal"
        :fields="deal_submodel_sections.location"
        :readonly="true"
      />
      <DealSection
        :title="deal_sections.general_info.label"
        :deal="deal"
        :sections="deal_sections.general_info.subsections"
        :readonly="true"
      />

      <DealSubmodelSection
        :title="`Contracts`"
        :entries="deal.contracts"
        :fields="deal_submodel_sections.contract"
        :readonly="true"
        model="contract"
      />

      <DealSection
        :title="deal_sections.employment.label"
        :deal="deal"
        :sections="deal_sections.employment.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_sections.investor_info.label"
        :deal="deal"
        :sections="deal_sections.investor_info.subsections"
        :readonly="true"
      />

      <DealSubmodelSection
        :title="`DataSources`"
        :entries="deal.datasources"
        :fields="deal_submodel_sections.datasource"
        :readonly="true"
        model="datasource"
      />

      <DealSection
        :title="deal_sections.local_communities.label"
        :deal="deal"
        :sections="deal_sections.local_communities.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_sections.former_use.label"
        :deal="deal"
        :sections="deal_sections.former_use.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_sections.produce_info.label"
        :deal="deal"
        :sections="deal_sections.produce_info.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_sections.water.label"
        :deal="deal"
        :sections="deal_sections.water.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_sections.gender_related_info.label"
        :deal="deal"
        :sections="deal_sections.gender_related_info.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_sections.guidelines_and_principles.label"
        :deal="deal"
        :sections="deal_sections.guidelines_and_principles.subsections"
        :readonly="true"
      />

      <b-tab disabled>
        <template v-slot:title>
          <hr />
        </template>
      </b-tab>

      <b-tab title="Deal History">
        <DealHistory :deal="deal" :deal_id="deal_id" :deal_version="deal_version" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import store from "/store";
  import DealSection from "/components/Deal/DealSection";
  import DealHistory from "/components/Deal/DealHistory";
  import DealLocationSection from "/components/Deal/DealLocationsSection";
  import DealSubmodelSection from "/components/Deal/DealSubmodelSection";
  import { deal_sections, deal_submodel_sections } from "./deal_sections";

  export default {
    props: ["deal_id", "deal_version"],
    components: {
      DealHistory,
      DealSection,
      DealLocationSection,
      DealSubmodelSection,
    },
    data() {
      return {
        loading: false,
        deal_sections,
        deal_submodel_sections,
      };
    },
    computed: {
      deal() {
        return this.$store.state.deal.current_deal;
      },
      not_public() {
        if (this.deal) {
          if (this.deal.status === 1 || this.deal.status === 6)
            return "This deal version is pending.";
          if (this.deal.status === 4)
            return "This deal has been deleted. It is not visible for public users.";
          if (this.deal.status === 5)
            return "This deal version has been rejected. It is not visible for public users.";
        }
        return null;
      },
    },
    beforeRouteEnter(to, from, next) {
      store
        .dispatch("setCurrentDeal", {
          deal_id: to.params.deal_id,
          deal_version: to.params.deal_version,
        })
        .then(() => next())
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
    beforeRouteUpdate(to, from, next) {
      this.loading = true;
      store
        .dispatch("setCurrentDeal", {
          deal_id: to.params.deal_id,
          deal_version: to.params.deal_version,
        })
        .then(() => {
          this.loading = false;
          next();
        })
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
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

  div.quicknav {
    z-index: 100;
    position: absolute;
    right: 200px;
    width: 200px;
    height: 100%;
    background: rgba(255, 255, 255, 0.7);
  }
</style>
