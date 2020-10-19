<template>
  <div class="container deal-detail" v-if="deal">
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
      content-class="mb-3"
      vertical
      pills
      nav-wrapper-class="position-relative"
      nav-class="sticky-nav"
      :key="deal_id + deal_version"
    >
      <DealLocationsSection
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
        :title="$t('Contracts')"
        :model_name="$t('Contract')"
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
        @activated="triggerInvestorGraphRefresh"
      >
        <div class="row">
          <div
            class="col-md-12 col-lg-10 col-xl-9"
            :class="{ loading_wrapper: this.$apollo.queries.investor.loading }"
          >
            <template v-if="investor.involvements.length">
              <h3 class="mb-2">
                Network of parent companies and tertiary investors/lenders
              </h3>
              <InvestorGraph
                :investor="investor"
                :showDeals="false"
                :controls="false"
                :depth="4"
                ref="investorGraph"
              ></InvestorGraph>
            </template>
            <div v-else class="loader"></div>
          </div>
        </div>
      </DealSection>

      <DealSubmodelSection
        :title="$t('Data Sources')"
        :model_name="$t('Data Source')"
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

      <DealSection
        :title="deal_sections.overall_comment.label"
        :deal="deal"
        :sections="deal_sections.overall_comment.subsections"
        :readonly="true"
      />

      <b-tab disabled>
        <template v-slot:title>
          <hr />
        </template>
      </b-tab>

      <DealSection
        :title="deal_sections.meta.label"
        :deal="deal"
        :sections="deal_sections.meta.subsections"
        :readonly="true"
      />

      <b-tab :title="$t('Deal History')">
        <DealHistory :deal="deal" :deal_id="deal_id" :deal_version="deal_version" />
      </b-tab>

      <b-tab :title="$t('Comments')">
        <DealComments :comments="deal.comments"></DealComments>
      </b-tab>

    </b-tabs>
  </div>
</template>

<script>
  import DealSection from "/components/Deal/DealSection";
  import DealHistory from "/components/Deal/DealHistory";
  import DealLocationsSection from "/components/Deal/DealLocationsSection";
  import DealSubmodelSection from "/components/Deal/DealSubmodelSection";
  import InvestorGraph from "/components/Investor/InvestorGraph";
  import { deal_sections, deal_submodel_sections } from "./deal_sections";
  import { deal_gql_query } from "./deal_fields";
  import gql from "graphql-tag";
  import store from "../../store";
  import DealComments from "../../components/Deal/DealComments";

  export default {
    props: ["deal_id", "deal_version"],
    components: {
      DealComments,
      InvestorGraph,
      DealHistory,
      DealSection,
      DealLocationsSection,
      DealSubmodelSection,
    },
    apollo: {
      deal: {
        query: deal_gql_query,
        variables() {
          return {
            id: +this.deal_id,
            version: +this.deal_version,
          };
        },
      },
      investor: {
        query: gql`
          query DealInvestor($id: Int!) {
            investor(id: $id) {
              id
              name
              involvements(depth: 3, include_ventures: false)
            }
          }
        `,
        variables() {
          return {
            id: +this.deal.operating_company.id,
          };
        },
        skip() {
          if (!this.deal) return true;
          if (!this.deal.operating_company) return true;
          return !this.deal.operating_company.id;
        },
      },
    },
    data() {
      return {
        deal: null,
        loading: false,
        deal_sections,
        deal_submodel_sections,
        investor: { involvements: [] },
      };
    },
    computed: {
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
    methods: {
      triggerInvestorGraphRefresh() {
        this.$refs.investorGraph.refresh_graph();
      },
      updatePageContext(to) {
        let title = `Deal #${to.params.deal_id}`;
        this.$store.dispatch("setPageContext", {
          title,
          breadcrumbs: [
            { link: { name: "wagtail" }, name: "Home" },
            { link: { name: "list_deals" }, name: "Deals" },
            { name: title },
          ],
        });
      }
    },
    beforeRouteEnter(to, from, next) {
      next(vm => {
        vm.updatePageContext(to);
      });
    },
    beforeRouteUpdate(to, from, next) {
      this.updatePageContext(to)
      next();
    },
  };
</script>
<style lang="scss">
  @import "../../scss/colors";

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
  .panel-body > h3 {
    margin-top: 1em;
    margin-bottom: 0.5em;
  }
  .panel-body:first-child > h3 {
    margin-top: 0.3em;
  }

  .deal-detail {
    .nav-pills {
      .nav-item {
        .nav-link {
          border-right: 1px solid $lm_orange;
          color: $lm_orange;
          border-radius: 0;

          &.active {
            border-right-width: 3px;
            background-color: inherit;
            color: $lm_dark;
          }
        }
      }
    }
  }
</style>
