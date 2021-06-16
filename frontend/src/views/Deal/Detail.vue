<template>
  <div v-if="deal">
    <ManageHeader
      v-if="manage"
      :deal="deal"
      :deal-version="dealVersion"
      @change_deal_status="change_deal_status"
      @reload_deal="reload_deal"
      @delete="deleteDeal"
      @set_confidential="setConfidential"
    />
    <div v-else class="container deal-detail">
      <div class="row">
        <div>
          <h1>
            Deal #{{ deal.id }}
            <span v-if="deal.country">in {{ deal.country.name }}</span>
          </h1>
        </div>
        <div class="ml-auto">
          <a
            v-if="$store.getters.userAuthenticated"
            :href="`/legacy/deal/edit/${deal.id}/`"
            target="_blank"
          >
            <i class="fas fa-edit"></i> {{ $t("Edit") }}
          </a>
          <HeaderDates :obj="deal" />
        </div>
      </div>
    </div>
    <div class="container deal-detail">
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
        content-class="mb-3 col-sm-7 col-md-9"
        vertical
        pills
        nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
        nav-class="sticky-nav"
      >
        <DealLocationsSection
          key="1"
          :deal="deal"
          :fields="deal_submodel_sections.location"
          :active="active_tab === '#locations'"
          @activated="updateRoute('#locations')"
        />
        <DealSection
          key="2"
          :title="deal_sections.general_info.label"
          :deal="deal"
          :sections="deal_sections.general_info.subsections"
          :active="active_tab === '#general'"
          @activated="updateRoute('#general')"
        />

        <DealSubmodelSection
          key="3"
          title="Contracts"
          model-name="Contract"
          :entries="deal.contracts"
          :fields="deal_submodel_sections.contract"
          model="contract"
          :active="active_tab === '#contracts'"
          @activated="updateRoute('#contracts')"
        />

        <DealSection
          key="4"
          :title="deal_sections.employment.label"
          :deal="deal"
          :sections="deal_sections.employment.subsections"
          :active="active_tab === '#employment'"
          @activated="updateRoute('#employment')"
        />

        <DealSection
          key="5"
          :title="deal_sections.investor_info.label"
          :deal="deal"
          :sections="deal_sections.investor_info.subsections"
          :active="active_tab === '#investor_info'"
          @activated="triggerInvestorGraphRefresh"
        >
          <div class="row">
            <div
              class="col-md-12 col-lg-10 col-xl-9"
              :class="{ loading_wrapper: $apollo.queries.investor.loading }"
            >
              <div
                v-if="investor && investor.involvements && investor.involvements.length"
              >
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
              </div>
              <div v-else class="loader"></div>
            </div>
          </div>
        </DealSection>

        <DealSubmodelSection
          key="6"
          title="Data sources"
          model-name="Data source"
          :entries="deal.datasources"
          :fields="deal_submodel_sections.datasource"
          model="datasource"
          :active="active_tab === '#data_sources'"
          @activated="updateRoute('#data_sources')"
        />

        <DealSection
          key="7"
          :title="deal_sections.local_communities.label"
          :deal="deal"
          :sections="deal_sections.local_communities.subsections"
          :active="active_tab === '#local_communities'"
          @activated="updateRoute('#local_communities')"
        />

        <DealSection
          key="8"
          :title="deal_sections.former_use.label"
          :deal="deal"
          :sections="deal_sections.former_use.subsections"
          :active="active_tab === '#former_use'"
          @activated="updateRoute('#former_use')"
        />

        <DealSection
          key="9"
          :title="deal_sections.produce_info.label"
          :deal="deal"
          :sections="deal_sections.produce_info.subsections"
          :active="active_tab === '#produce_info'"
          @activated="updateRoute('#produce_info')"
        />

        <DealSection
          key="10"
          :title="deal_sections.water.label"
          :deal="deal"
          :sections="deal_sections.water.subsections"
          :active="active_tab === '#water'"
          @activated="updateRoute('#water')"
        />

        <DealSection
          key="11"
          :title="deal_sections.gender_related_info.label"
          :deal="deal"
          :sections="deal_sections.gender_related_info.subsections"
          :active="active_tab === '#gender_related_info'"
          @activated="updateRoute('#gender_related_info')"
        />

        <DealSection
          key="12"
          :title="deal_sections.guidelines_and_principles.label"
          :deal="deal"
          :sections="deal_sections.guidelines_and_principles.subsections"
          :active="active_tab === '#guidelines_and_principles'"
          @activated="updateRoute('#guidelines_and_principles')"
        />

        <DealSection
          key="13"
          :title="deal_sections.overall_comment.label"
          :deal="deal"
          :sections="deal_sections.overall_comment.subsections"
          :active="active_tab === '#overall_comment'"
          @activated="updateRoute('#overall_comment')"
        />

        <b-tab key="14" disabled>
          <template #title>
            <hr />
          </template>
        </b-tab>

        <b-tab
          key="15"
          :title="$t('Deal history')"
          :active="active_tab === '#history'"
          @click="updateRoute('#history')"
        >
          <DealHistory :deal="deal" :deal-id="dealId" :deal-version="dealVersion" />
        </b-tab>

        <b-tab
          key="16"
          :title="$t('Comments')"
          :active="active_tab === '#comments'"
          @click="updateRoute('#comments')"
        >
          <DealComments :comments="deal.comments"></DealComments>
        </b-tab>

        <b-tab
          key="17"
          :title="$t('Actions')"
          :active="active_tab === '#actions'"
          @click="updateRoute('#actions')"
        >
          <h4><i class="fa fa-download"></i> Download</h4>
          <a :href="download_link('xlsx')">XLSX</a><br />
          <a :href="download_link('csv')">CSV</a>
        </b-tab>
      </b-tabs>
    </div>
  </div>
  <div v-else>
    <LoadingPulse></LoadingPulse>
  </div>
</template>

<script>
  import DealComments from "$components/Deal/DealComments";
  import DealHistory from "$components/Deal/DealHistory";
  import DealLocationsSection from "$components/Deal/DealLocationsSection";
  import DealSection from "$components/Deal/DealSection";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection";
  import ManageHeader from "$components/Deal/ManageHeader";
  import HeaderDates from "$components/HeaderDates";
  import InvestorGraph from "$components/Investor/InvestorGraph";
  import { deal_gql_query } from "$store/queries";

  import gql from "graphql-tag";
  import { mapState } from "vuex";

  import { deal_sections, deal_submodel_sections } from "./deal_sections";
  import LoadingPulse from "$components/Data/LoadingPulse";

  function equalDealParams(from_params, to_params) {
    if (parseInt(from_params.dealId) !== parseInt(to_params.dealId)) return false;
    if ("dealVersion" in from_params && "dealVersion" in to_params) {
      if (parseInt(from_params.dealVersion) !== parseInt(to_params.dealVersion))
        return false;
    } else {
      return false;
    }
    return true;
  }

  export default {
    name: "Detail",
    components: {
      LoadingPulse,
      HeaderDates,
      DealComments,
      DealHistory,
      DealLocationsSection,
      DealSection,
      DealSubmodelSection,
      InvestorGraph,
      ManageHeader,
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        console.log("Deal detail: Route enter");
        vm.updatePageContext(to);
        if (!to.hash) {
          vm.active_tab = "#locations";
        }
      });
    },
    beforeRouteUpdate(to, from, next) {
      console.log("Deal detail: Route update");
      this.updatePageContext(to);
      next();
    },
    props: {
      dealId: { type: [Number, String], required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    metaInfo() {
      return { title: this.title };
    },
    data() {
      return {
        deal: null,
        deal_sections,
        deal_submodel_sections,
        investor: { involvements: [] },
        title: "Deal",
        active_tab: "#locations",
      };
    },
    apollo: {
      deal: {
        query: deal_gql_query,
        variables() {
          return {
            id: +this.dealId,
            version: this.dealVersion ? +this.dealVersion : null,
            subset: this.$store.getters.userAuthenticated ? "UNFILTERED" : "PUBLIC",
          };
        },
        update({ deal }) {
          if (!deal && !this.$store.getters.userAuthenticated)
            this.$router.push({ name: "login", query: { next: this.$route.fullPath } });
          if (!deal) this.$router.push({ name: "list_deals" });
          if (deal.status === 1 && !this.dealVersion)
            this.$router.push({
              name: "deal_detail",
              params: {
                dealId: this.dealId,
                dealVersion: deal.versions[0].revision.id,
              },
            });
          return deal;
        },
        fetchPolicy: "network-only",
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
      current_deal_query_vars() {},
      manage() {
        return (
          this.$store.state.page.user && this.$store.state.page.user.is_authenticated
        );
      },
      ...mapState({
        formFields: (state) => state.formfields,
      }),
    },
    methods: {
      change_deal_status({ transition, comment = null, to_user = null }) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation (
                $id: Int!
                $version: Int!
                $transition: WorkflowTransition!
                $comment: String
                $to_user_id: Int
              ) {
                change_deal_status(
                  id: $id
                  version: $version
                  transition: $transition
                  comment: $comment
                  to_user_id: $to_user_id
                ) {
                  dealId
                  dealVersion
                }
              }
            `,
            variables: {
              id: +this.dealId,
              version: this.dealVersion ? +this.dealVersion : null,
              transition,
              comment,
              to_user_id: to_user ? to_user.id : null,
            },
          })
          .then(({ data: { change_deal_status } }) => {
            if (transition === "ACTIVATE") {
              this.$router.push({
                name: "deal_detail",
                params: { dealId: change_deal_status.dealId.toString() },
              });
            } else {
              if (parseInt(this.dealVersion) !== change_deal_status.dealVersion) {
                this.$router.push({
                  name: "deal_detail",
                  params: {
                    dealId: change_deal_status.dealId.toString(),
                    dealVersion: change_deal_status.dealVersion.toString(),
                  },
                });
              } else {
                this.$apollo.queries.deal.refetch();
              }
            }
          })
          .catch((error) => console.error(error));
      },
      deleteDeal(comment) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation ($id: Int!, $version: Int, $comment: String) {
                deal_delete(id: $id, version: $version, comment: $comment)
              }
            `,
            variables: {
              id: +this.dealId,
              version: this.dealVersion ? +this.dealVersion : null,
              comment,
            },
          })
          .then(() => {
            if (this.dealVersion) {
              this.$router
                .push({
                  name: "deal_detail",
                  params: { dealId: this.dealId.toString() },
                })
                .then(this.$apollo.queries.deal.refetch);
            }
            this.$apollo.queries.deal.refetch();
          });
      },
      setConfidential(data) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation (
                $id: Int!
                $confidential: Boolean!
                $version: Int
                $reason: ConfidentialReason
                $comment: String
              ) {
                deal_set_confidential(
                  id: $id
                  confidential: $confidential
                  version: $version
                  reason: $reason
                  comment: $comment
                )
              }
            `,
            variables: {
              id: +this.dealId,
              version: this.dealVersion ? +this.dealVersion : null,
              confidential: data.confidential,
              reason: data.reason,
              comment: data.comment,
            },
          })
          .then(() => {
            this.$apollo.queries.deal.refetch();
          });
      },
      updateRoute(emiter) {
        console.log("Deal detail: update route");
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
      },
      triggerInvestorGraphRefresh() {
        console.log("Deal detail: investor graph refresh");
        this.updateRoute("#investor_info");
        if ("investorGraph" in this.$refs) {
          this.$refs.investorGraph.refresh_graph();
        }
      },
      updatePageContext(to) {
        console.log("Deal detail: update page context");
        if (to.hash) {
          // only update if hash is present (otherwise #locations are active by default)
          this.active_tab = to.hash;
        }
        this.title = `Deal #${to.params.dealId}`;
        this.$store.dispatch("setPageContext", {
          breadcrumbs: [
            { link: { name: "wagtail" }, name: "Home" },
            { link: { name: "list_deals" }, name: "Deals" },
            { name: this.title },
          ],
        });
      },
      download_link(format) {
        return `/api/legacy_export/?deal_id=${this.deal.id}&subset=UNFILTERED&format=${format}`;
      },
      reload_deal() {
        console.log("Deal detail: reload");
        this.$apollo.queries.deal.refetch();
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
</style>
