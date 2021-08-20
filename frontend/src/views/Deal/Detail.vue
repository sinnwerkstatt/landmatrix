<template>
  <div v-if="deal">
    <DealManageHeader
      v-if="userAuthenticated"
      :deal="deal"
      :deal-version="dealVersion"
      @change_status="changeStatus"
      @delete="deleteDeal"
      @reload="reloadDeal"
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
          <HeaderDates :obj="deal" />
        </div>
      </div>
    </div>

    <div class="container deal-detail">
      <b-tabs
        id="tabNav"
        :key="dealId + dealVersion"
        content-class="mb-3 col-sm-7 col-md-9"
        nav-class="sticky-nav"
        nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
        pills
        vertical
      >
        <DealLocationsSection
          key="1"
          :active="active_tab === '#locations'"
          :deal="deal"
          :fields="deal_submodel_sections.location"
          @activated="updateRoute('#locations')"
        />
        <DealSection
          key="2"
          :active="active_tab === '#general'"
          :deal="deal"
          :sections="deal_sections.general_info.subsections"
          :title="deal_sections.general_info.label"
          @activated="updateRoute('#general')"
        />

        <DealSubmodelSection
          key="3"
          :active="active_tab === '#contracts'"
          :entries="deal.contracts"
          :fields="deal_submodel_sections.contract"
          model="contract"
          model-name="Contract"
          title="Contracts"
          @activated="updateRoute('#contracts')"
        />

        <DealSection
          key="4"
          :active="active_tab === '#employment'"
          :deal="deal"
          :sections="deal_sections.employment.subsections"
          :title="deal_sections.employment.label"
          @activated="updateRoute('#employment')"
        />

        <DealSection
          key="5"
          :active="active_tab === '#investor_info'"
          :deal="deal"
          :sections="deal_sections.investor_info.subsections"
          :title="deal_sections.investor_info.label"
          @activated="triggerInvestorGraphRefresh"
        >
          <div class="row">
            <div
              :class="{ loading_wrapper: $apollo.queries.investor.loading }"
              class="col-md-12 col-lg-10 col-xl-9"
            >
              <div
                v-if="investor && investor.involvements && investor.involvements.length"
              >
                <h3 class="mb-2">
                  Network of parent companies and tertiary investors/lenders
                </h3>
                <InvestorGraph
                  ref="investorGraph"
                  :controls="false"
                  :init-depth="4"
                  :investor="investor"
                  :show-deals-on-load="false"
                />
              </div>
              <div v-else class="loader"></div>
            </div>
          </div>
        </DealSection>

        <DealSubmodelSection
          key="6"
          :active="active_tab === '#data_sources'"
          :entries="deal.datasources"
          :fields="deal_submodel_sections.datasource"
          model="datasource"
          model-name="Data source"
          title="Data sources"
          @activated="updateRoute('#data_sources')"
        />

        <DealSection
          key="7"
          :active="active_tab === '#local_communities'"
          :deal="deal"
          :sections="deal_sections.local_communities.subsections"
          :title="deal_sections.local_communities.label"
          @activated="updateRoute('#local_communities')"
        />

        <DealSection
          key="8"
          :active="active_tab === '#former_use'"
          :deal="deal"
          :sections="deal_sections.former_use.subsections"
          :title="deal_sections.former_use.label"
          @activated="updateRoute('#former_use')"
        />

        <DealSection
          key="9"
          :active="active_tab === '#produce_info'"
          :deal="deal"
          :sections="deal_sections.produce_info.subsections"
          :title="deal_sections.produce_info.label"
          @activated="updateRoute('#produce_info')"
        />

        <DealSection
          key="10"
          :active="active_tab === '#water'"
          :deal="deal"
          :sections="deal_sections.water.subsections"
          :title="deal_sections.water.label"
          @activated="updateRoute('#water')"
        />

        <DealSection
          key="11"
          :active="active_tab === '#gender_related_info'"
          :deal="deal"
          :sections="deal_sections.gender_related_info.subsections"
          :title="deal_sections.gender_related_info.label"
          @activated="updateRoute('#gender_related_info')"
        />

        <DealSection
          key="12"
          :active="active_tab === '#guidelines_and_principles'"
          :deal="deal"
          :sections="deal_sections.guidelines_and_principles.subsections"
          :title="deal_sections.guidelines_and_principles.label"
          @activated="updateRoute('#guidelines_and_principles')"
        />

        <DealSection
          key="13"
          :active="active_tab === '#overall_comment'"
          :deal="deal"
          :sections="deal_sections.overall_comment.subsections"
          :title="deal_sections.overall_comment.label"
          @activated="updateRoute('#overall_comment')"
        />

        <b-tab key="14" disabled>
          <template #title>
            <hr />
          </template>
        </b-tab>

        <b-tab
          key="15"
          :active="active_tab === '#history'"
          :title="$t('Deal history')"
          @click="updateRoute('#history')"
        >
          <DealHistory :deal="deal" :deal-id="dealId" :deal-version="dealVersion" />
        </b-tab>

        <b-tab
          key="16"
          :active="active_tab === '#comments'"
          :title="$t('Comments')"
          @click="updateRoute('#comments')"
        >
          <DealComments :deal-id="dealId" :comments="deal.comments" />
        </b-tab>

        <b-tab
          key="17"
          :active="active_tab === '#actions'"
          :title="$t('Actions')"
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
    <div v-if="$apollo.loading">
      <LoadingPulse></LoadingPulse>
    </div>
    <div v-if="loadingError" class="container">
      <div>{{ $t("Could not load this deal") }}</div>
      <span class="small">{{ $t("Maybe you forgot to login?") }}</span>
    </div>
  </div>
</template>

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";

  import DealHistory from "$components/Deal/DealHistory";
  import DealLocationsSection from "$components/Deal/DealLocationsSection";
  import DealManageHeader from "$components/Deal/DealManageHeader";
  import DealSection from "$components/Deal/DealSection";
  import DealSubmodelSection from "$components/Deal/DealSubmodelSection";
  import HeaderDates from "$components/HeaderDates";
  import InvestorGraph from "$components/Investor/InvestorGraph";
  import { deal_gql_query } from "$store/queries";
  import gql from "graphql-tag";
  import { deal_sections, deal_submodel_sections } from "./deal_sections";

  // function equalDealParams(from_params, to_params) {
  //   if (parseInt(from_params.dealId) !== parseInt(to_params.dealId)) return false;
  //   if ("dealVersion" in from_params && "dealVersion" in to_params) {
  //     if (parseInt(from_params.dealVersion) !== parseInt(to_params.dealVersion))
  //       return false;
  //   } else {
  //     return false;
  //   }
  //   return true;
  // }

  export default {
    name: "Detail",
    components: {
      DealComments: () => import("$components/Deal/DealComments"),
      DealHistory,
      DealLocationsSection,
      DealManageHeader,
      DealSection,
      DealSubmodelSection,
      HeaderDates,
      InvestorGraph,
      LoadingPulse,
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
        loadingError: false,
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
                dealVersion: deal.versions[0].id,
              },
            });
          return deal;
        },
        error(e) {
          this.loadingError = true;
          console.log({ e });
        },
        fetchPolicy: "no-cache",
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
      userAuthenticated() {
        return this.$store.state.page.user?.is_authenticated;
      },
    },
    methods: {
      changeStatus({ transition, comment = "", to_user = null }) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation (
                $id: Int!
                $version: Int!
                $transition: WorkflowTransition!
                $comment: String
                $to_user_id: Int
                $fully_updated: Boolean
              ) {
                change_deal_status(
                  id: $id
                  version: $version
                  transition: $transition
                  comment: $comment
                  to_user_id: $to_user_id
                  fully_updated: $fully_updated
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
              fully_updated: this.deal.fully_updated,
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
                this.reloadDeal();
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
                .then(this.reloadDeal);
            }
            this.reloadDeal();
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
          .then(this.reloadDeal);
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
      reloadDeal() {
        console.log("Deal detail: reload");
        this.$apollo.queries.deal.refetch();
      },
    },
  };
</script>

<style lang="scss">
  .headercountry {
    white-space: nowrap;
    display: block;
    font-size: 1rem;
  }

  .sticky-nav {
    position: -webkit-sticky;
    position: sticky;
    top: 8em;
    z-index: 99;
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
      color: var(--color-lm-dark);
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
          border-right: 1px solid var(--color-lm-orange);
          color: var(--color-lm-orange);
          border-radius: 0;

          &.active {
            border-right-width: 3px;
            background-color: inherit;
            color: var(--color-lm-dark);
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
