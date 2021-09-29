<template>
  <div v-if="deal" class="deal-detail-container">
    <DealManageHeader
      v-if="userAuthenticated"
      :deal="deal"
      :deal-version="dealVersion"
      @change_status="changeStatus"
      @delete="deleteDeal"
      @reload="reloadDeal"
      @set_confidential="setConfidential"
    />
    <div v-else class="simple-header container">
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

    <div class="deal-detail">
      <div class="deal-detail-nav">
        <SideTabsMenu :tabs="tabs" :active-tab="activeTab" @updateRoute="updateRoute" />
      </div>
      <div class="deal-detail-content">
        <DealLocationsSection
          v-if="activeTab === '#locations'"
          :deal="deal"
          :fields="deal_submodel_sections.location"
        />

        <DealSection
          v-if="activeTab === '#general'"
          :deal="deal"
          :sections="deal_sections.general_info.subsections"
        />

        <DealSubmodelSection
          v-if="activeTab === '#contracts'"
          :entries="deal.contracts"
          :fields="deal_submodel_sections.contract"
          model="contract"
          model-name="Contract"
        />

        <DealSection
          v-if="activeTab === '#employment'"
          :deal="deal"
          :sections="deal_sections.employment.subsections"
        />

        <DealSection
          v-if="activeTab === '#investor_info'"
          :deal="deal"
          :sections="deal_sections.investor_info.subsections"
        >
          <div :class="{ loading_wrapper: $apollo.queries.investor.loading }">
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
        </DealSection>

        <DealSubmodelSection
          v-if="activeTab === '#data_sources'"
          :entries="deal.datasources"
          :fields="deal_submodel_sections.datasource"
          model="datasource"
          model-name="Data source"
        />

        <DealSection
          v-if="activeTab === '#local_communities'"
          :deal="deal"
          :sections="deal_sections.local_communities.subsections"
        />

        <DealSection
          v-if="activeTab === '#former_use'"
          :deal="deal"
          :sections="deal_sections.former_use.subsections"
        />

        <DealSection
          v-if="activeTab === '#produce_info'"
          :deal="deal"
          :sections="deal_sections.produce_info.subsections"
        />

        <DealSection
          v-if="activeTab === '#water'"
          :deal="deal"
          :sections="deal_sections.water.subsections"
        />

        <DealSection
          v-if="activeTab === '#gender_related_info'"
          :deal="deal"
          :sections="deal_sections.gender_related_info.subsections"
        />

        <DealSection
          v-if="activeTab === '#overall_comment'"
          :deal="deal"
          :sections="deal_sections.overall_comment.subsections"
        />

        <section v-if="activeTab === '#history'">
          <DealHistory :deal="deal" :deal-id="dealId" :deal-version="dealVersion" />
        </section>

        <section v-if="activeTab === '#comments'">
          <DealComments :deal-id="dealId" :comments="deal.comments" />
        </section>

        <section v-if="activeTab === '#actions'">
          <h4><i class="fa fa-download"></i> Download</h4>
          <a :href="download_link('xlsx')">XLSX</a><br />
          <a :href="download_link('csv')">CSV</a>
        </section>
      </div>
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
  import SideTabsMenu from "$components/Shared/SideTabsMenu";
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
      SideTabsMenu,
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
          vm.activeTab = "#locations";
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
        activeTab: "#locations",
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
                dealVersion: deal.versions[0]?.id,
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
      tabs() {
        return {
          locations: this.$t("Locations"),
          general: this.$t("General info"),
          contracts: this.$t("Contracts"),
          employment: this.$t("Employment"),
          investor_info: this.$t("Investor info"),
          data_sources: this.$t("Data sources"),
          local_communities: this.$t("Local communities / indigenous peoples"),
          former_use: this.$t("Former use"),
          produce_info: this.$t("Produce info"),
          water: this.$t("Water"),
          gender_related_info: this.$t("Gender-related info"),
          overall_comment: this.$t("Overall comment"),
          blank1: null,
          history: this.$t("Deal History"),
          comments: this.$t("Comments"),
          actions: this.$t("Actions"),
        };
      },
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
        console.log({ emiter });
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
          this.activeTab = to.hash;
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
  .deal-detail-container {
    overflow: hidden;
    overflow-y: auto;
    height: calc(100vh - 60px - 31px);
    width: 100vw;
  }

  .deal-detail {
    width: clamp(20rem, 86vw, 75rem);
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    overflow: hidden;
    position: relative;
    margin: 0 auto;
  }
  .deal-detail-nav {
    height: 100%;
    grid-column: span 3;
    @media only screen and (max-width: 992px) {
      grid-column: span 12;
    }
  }

  .deal-detail-content {
    height: 100%;
    grid-column: span 9;
    //overflow-y: auto;
    @media only screen and (max-width: 992px) {
      grid-column: span 12;
    }
  }

  .simple-header {
    h1 {
      color: var(--color-lm-dark);
      text-align: left;
      text-transform: none;

      &:before {
        display: none;
      }
    }
  }
</style>
