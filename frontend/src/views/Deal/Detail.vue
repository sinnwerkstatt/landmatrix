<template>
  <div v-if="deal" class="container deal-detail">
    <div class="row">
      <div class="col-sm-5 col-md-3">
        <h1>Deal #{{ deal.id }}</h1>
      </div>
      <div class="col-sm-7 col-md-9 panel-container">
        <a
          v-if="$store.getters.userAuthenticated"
          :href="`/legacy/deal/edit/${deal.id}/`"
          target="_blank"
        >
          <i class="fas fa-edit"></i> {{ $t("Edit") }}
        </a>
        <div class="meta-panel">
          <DisplayField
            :wrapper-classes="['inlinefield']"
            :label-classes="['inlinelabel']"
            :value-classes="['inlineval']"
            fieldname="created_at"
            :value="deal.created_at"
          />
          <DisplayField
            :wrapper-classes="['inlinefield']"
            :label-classes="['inlinelabel']"
            :value-classes="['inlineval']"
            fieldname="modified_at"
            :value="deal.modified_at"
          />
          <DisplayField
            :wrapper-classes="['inlinefield']"
            :label-classes="['inlinelabel']"
            :value-classes="['inlineval']"
            fieldname="fully_updated_at"
            :value="deal.fully_updated_at"
            :visible="!!deal.fully_updated_at"
          />
        </div>
      </div>
    </div>

    <p v-if="not_public" class="alert alert-danger mb-4">{{ $t(not_public) }}</p>
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
      id="tabNav"
      :key="dealId + dealVersion"
      content-class="mb-3"
      vertical
      pills
      nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
      nav-class="sticky-nav"
    >
      <DealLocationsSection
        :deal="deal"
        :fields="deal_submodel_sections.location"
        :active="active_tab === '#locations'"
        @activated="updateRoute('#locations')"
      />
      <DealSection
        :title="deal_sections.general_info.label"
        :deal="deal"
        :sections="deal_sections.general_info.subsections"
        :active="active_tab === '#general'"
        @activated="updateRoute('#general')"
      />

      <DealSubmodelSection
        title="Contracts"
        model-name="Contract"
        :entries="deal.contracts"
        :fields="deal_submodel_sections.contract"
        model="contract"
        :active="active_tab === '#contracts'"
        @activated="updateRoute('#contracts')"
      />

      <DealSection
        :title="deal_sections.employment.label"
        :deal="deal"
        :sections="deal_sections.employment.subsections"
        :active="active_tab === '#employment'"
        @activated="updateRoute('#employment')"
      />

      <DealSection
        :title="deal_sections.investor_info.label"
        :deal="deal"
        :sections="deal_sections.investor_info.subsections"
        :active="active_tab === '#investor_info'"
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
                ref="investorGraph"
                :investor="investor"
                :show-deals-on-load="false"
                :controls="false"
                :init-depth="4"
              />
            </template>
            <div v-else class="loader"></div>
          </div>
        </div>
      </DealSection>

      <DealSubmodelSection
        title="Data Sources"
        model-name="Data Source"
        :entries="deal.datasources"
        :fields="deal_submodel_sections.datasource"
        model="datasource"
        :active="active_tab === '#data_sources'"
        @activated="updateRoute('#data_sources')"
      />

      <DealSection
        :title="deal_sections.local_communities.label"
        :deal="deal"
        :sections="deal_sections.local_communities.subsections"
        :active="active_tab === '#local_communities'"
        @activated="updateRoute('#local_communities')"
      />

      <DealSection
        :title="deal_sections.former_use.label"
        :deal="deal"
        :sections="deal_sections.former_use.subsections"
        :active="active_tab === '#former_use'"
        @activated="updateRoute('#former_use')"
      />

      <DealSection
        :title="deal_sections.produce_info.label"
        :deal="deal"
        :sections="deal_sections.produce_info.subsections"
        :active="active_tab === '#produce_info'"
        @activated="updateRoute('#produce_info')"
      />

      <DealSection
        :title="deal_sections.water.label"
        :deal="deal"
        :sections="deal_sections.water.subsections"
        :active="active_tab === '#water'"
        @activated="updateRoute('#water')"
      />

      <DealSection
        :title="deal_sections.gender_related_info.label"
        :deal="deal"
        :sections="deal_sections.gender_related_info.subsections"
        :active="active_tab === '#gender_related_info'"
        @activated="updateRoute('#gender_related_info')"
      />

      <DealSection
        :title="deal_sections.guidelines_and_principles.label"
        :deal="deal"
        :sections="deal_sections.guidelines_and_principles.subsections"
        :active="active_tab === '#guidelines_and_principles'"
        @activated="updateRoute('#guidelines_and_principles')"
      />

      <DealSection
        :title="deal_sections.overall_comment.label"
        :deal="deal"
        :sections="deal_sections.overall_comment.subsections"
        :active="active_tab === '#overall_comment'"
        @activated="updateRoute('#overall_comment')"
      />

      <b-tab disabled>
        <template #title>
          <hr />
        </template>
      </b-tab>

      <b-tab
        :title="$t('Deal History')"
        :active="active_tab === '#history'"
        @click="updateRoute('#history')"
      >
        <DealHistory :deal="deal" :deal-id="dealId" :deal-version="dealVersion" />
      </b-tab>

      <b-tab
        :title="$t('Comments')"
        :active="active_tab === '#comments'"
        @click="updateRoute('#comments')"
      >
        <DealComments :comments="deal.comments"></DealComments>
      </b-tab>

      <b-tab
        :title="$t('Actions')"
        :active="active_tab === '#actions'"
        @click="updateRoute('#actions')"
      >
        <h4><i class="fa fa-download"></i> Download</h4>
        <a :href="`/api/legacy_export/?deal_id=${deal.id}&format=xlsx`">XLSX</a><br />
        <a :href="`/api/legacy_export/?deal_id=${deal.id}&format=csv`">CSV</a>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import gql from "graphql-tag";
  import { mapState } from "vuex";

  import { deal_sections, deal_submodel_sections } from "./deal_sections";
  import { deal_gql_query } from "store/queries";

  import DealSection from "components/Deal/DealSection";
  import DealHistory from "components/Deal/DealHistory";
  import DealLocationsSection from "components/Deal/DealLocationsSection";
  import DealSubmodelSection from "components/Deal/DealSubmodelSection";
  import InvestorGraph from "components/Investor/InvestorGraph";
  import DealComments from "components/Deal/DealComments";
  import DisplayField from "components/Fields/DisplayField";

  export default {
    components: {
      DisplayField,
      DealComments,
      InvestorGraph,
      DealHistory,
      DealSection,
      DealLocationsSection,
      DealSubmodelSection,
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.updatePageContext(to);
      });
    },
    beforeRouteUpdate(to, from, next) {
      this.updatePageContext(to);
      next();
    },
    props: {
      dealId: { type: [Number, String], required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        deal: null,

        deal_sections,
        deal_submodel_sections,
        investor: { involvements: [] },
      };
    },
    apollo: {
      deal: {
        query: deal_gql_query,
        variables() {
          return {
            id: +this.dealId,
            version: +this.dealVersion,
            subset: this.$store.state.page.user ? "UNFILTERED" : "PUBLIC",
          };
        },
        update(data) {
          if (!data.deal) {
            this.$router.push({
              name: "404",
              params: [this.$router.currentRoute.path],
              replace: true,
            });
          }
          return data.deal;
        },
      },
      investor: {
        query: gql`
          query DealInvestor($id: Int!) {
            investor(
              id: $id
              involvements_depth: 5
              involvements_include_ventures: false
            ) {
              id
              name
              classification
              country {
                id
                name
              }
              homepage
              comment
              involvements
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
    computed: {
      active_tab() {
        return location.hash ? location.hash : "#locations";
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
      ...mapState({
        formFields: (state) => state.formfields,
      }),
    },
    methods: {
      updateRoute(emiter) {
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
      },
      triggerInvestorGraphRefresh() {
        this.updateRoute("#investor_info");
        if ("investorGraph" in this.$refs) {
          this.$refs.investorGraph.refresh_graph();
        }
      },
      updatePageContext(to) {
        let title = `Deal #${to.params.dealId}`;
        this.$store.dispatch("setPageContext", {
          title,
          breadcrumbs: [
            { link: { name: "wagtail" }, name: "Home" },
            { link: { name: "list_deals" }, name: "Deals" },
            { name: title },
          ],
        });
      },
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";

  .sticky-nav {
    position: -webkit-sticky;
    position: sticky;
    top: 8em;
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
    h1 {
      color: $lm_dark;
      text-align: left;
      text-transform: none;

      &:before {
        display: none;
      }
    }

    .nav-pills {
      .nav-item {
        .nav-link {
          padding-left: 0;
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

    .sticky-top {
      top: 5em;
      z-index: 90;
    }
  }

  .panel-container {
    text-align: right;

    .meta-panel {
      text-align: left;
      display: inline-block;
      background-color: darken(white, 2);
      padding: 0.5em 1em;
      border-radius: 5px;
      font-size: 0.9rem;
      color: rgba(0, 0, 0, 0.25);

      .inlinefield {
        display: inline-block;

        &:not(:last-child) {
          margin-right: 1em;
        }

        .inlinelabel {
          display: inline-block;
          color: rgba(0, 0, 0, 0.3);
        }

        .inlineval {
          display: inline-block;
          font-style: italic;
        }
      }
    }
  }
</style>
