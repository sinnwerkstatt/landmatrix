<template>
  <div v-if="deal" class="container deal-edit">
    <b-tabs
      id="tabNav"
      :key="dealId + dealVersion"
      content-class="mb-3"
      vertical
      pills
      nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
      nav-class="sticky-nav"
    >
      <b-tab
        title="Locations"
        :active="active_tab === '#locations'"
        @click="updateRoute('#locations')"
      >
        <MapEditor :deal="deal" />
      </b-tab>
      <DealEditSection
        :title="deal_sections.general_info.label"
        :deal="deal"
        :sections="deal_sections.general_info.subsections"
        :active="active_tab === '#general'"
        @activated="updateRoute('#general')"
      />
      <DealSubmodelEditSection
        title="Contracts"
        model-name="Contract"
        :entries="deal.contracts"
        :fields="deal_submodel_sections.contract"
        model="contract"
        :active="active_tab === '#contracts'"
        @activated="updateRoute('#contracts')"
        @addEntry="addContract"
      />
      <DealEditSection
        :title="deal_sections.employment.label"
        :deal="deal"
        :sections="deal_sections.employment.subsections"
        :active="active_tab === '#employment'"
        @activated="updateRoute('#employment')"
      />

      <DealEditSection
        :title="deal_sections.investor_info.label"
        :deal="deal"
        :sections="deal_sections.investor_info.subsections"
        :active="active_tab === '#investor_info'"
        @activated="updateRoute('#investor_info')"
      >
        <!--        <div class="row">-->
        <!--          <div-->
        <!--            class="col-md-12 col-lg-10 col-xl-9"-->
        <!--            :class="{ loading_wrapper: this.$apollo.queries.investor.loading }"-->
        <!--          >-->
        <!--            <template v-if="investor.involvements.length">-->
        <!--              <h3 class="mb-2">-->
        <!--                Network of parent companies and tertiary investors/lenders-->
        <!--              </h3>-->
        <!--              <InvestorGraph-->
        <!--                ref="investorGraph"-->
        <!--                :investor="investor"-->
        <!--                :show-deals-on-load="false"-->
        <!--                :controls="false"-->
        <!--                :init-depth="4"-->
        <!--              />-->
        <!--            </template>-->
        <!--            <div v-else class="loader"></div>-->
        <!--          </div>-->
        <!--        </div>-->
      </DealEditSection>

      <DealSubmodelEditSection
        title="Data Sources"
        model-name="Data Source"
        :entries="deal.datasources"
        :fields="deal_submodel_sections.datasource"
        model="datasource"
        :active="active_tab === '#data_sources'"
        @activated="updateRoute('#data_sources')"
        @addEntry="addDataSource"
      />

      <DealEditSection
        :title="deal_sections.local_communities.label"
        :deal="deal"
        :sections="deal_sections.local_communities.subsections"
        :active="active_tab === '#local_communities'"
        @activated="updateRoute('#local_communities')"
      />

      <DealEditSection
        :title="deal_sections.former_use.label"
        :deal="deal"
        :sections="deal_sections.former_use.subsections"
        :active="active_tab === '#former_use'"
        @activated="updateRoute('#former_use')"
      />

      <DealEditSection
        :title="deal_sections.produce_info.label"
        :deal="deal"
        :sections="deal_sections.produce_info.subsections"
        :active="active_tab === '#produce_info'"
        @activated="updateRoute('#produce_info')"
      />

      <DealEditSection
        :title="deal_sections.water.label"
        :deal="deal"
        :sections="deal_sections.water.subsections"
        :active="active_tab === '#water'"
        @activated="updateRoute('#water')"
      />

      <DealEditSection
        :title="deal_sections.gender_related_info.label"
        :deal="deal"
        :sections="deal_sections.gender_related_info.subsections"
        :active="active_tab === '#gender_related_info'"
        @activated="updateRoute('#gender_related_info')"
      />

      <DealEditSection
        :title="deal_sections.guidelines_and_principles.label"
        :deal="deal"
        :sections="deal_sections.guidelines_and_principles.subsections"
        :active="active_tab === '#guidelines_and_principles'"
        @activated="updateRoute('#guidelines_and_principles')"
      />

      <DealEditSection
        :title="deal_sections.overall_comment.label"
        :deal="deal"
        :sections="deal_sections.overall_comment.subsections"
        :active="active_tab === '#overall_comment'"
        @activated="updateRoute('#overall_comment')"
      />
    </b-tabs>
  </div>
</template>

<script>
  import DealEditSection from "$components/Deal/DealEditSection";
  import DealSubmodelEditSection from "$components/Deal/DealSubmodelEditSection";
  import MapEditor from "$components/MapEditor";
  import { deal_gql_query } from "$store/queries";

  import { deal_sections, deal_submodel_sections } from "./deal_sections";

  export default {
    name: "DealEdit",
    components: { DealSubmodelEditSection, MapEditor, DealEditSection },
    props: {
      dealId: { type: [Number, String], required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        deal: null,
        deal_sections,
        deal_submodel_sections,
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
    },
    computed: {
      active_tab() {
        return location.hash ? location.hash : "#locations";
      },
    },
    methods: {
      updateRoute(emiter) {
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
      },
      addContract() {
        this.deal.contracts.push(
          new Object({
            number: "",
            date: null,
            expiration_date: null,
            agreement_duration: null,
            comment: "",
          })
        );
      },
      addDataSource() {
        this.deal.datasources.push(
          new Object({
            type: "",
            url: "",
            file: "",
            file_not_public: false,
            publication_title: "",
            date: "",
            name: "",
            company: "",
            email: "",
            phone: "",
            includes_in_country_verified_information: null,
            open_land_contracts_id: "",
            comment: "",
          })
        );
      },
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";

  .deal-edit {
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
