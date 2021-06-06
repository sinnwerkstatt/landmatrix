<template>
  <form @submit.prevent="deal_save">
    <div v-if="deal" class="container deal-edit">
      <h1 v-if="dealId">
        Editing Deal #{{ dealId }} in {{ deal.country && deal.country.name }}
      </h1>
      <h1 v-else>
        Adding new deal <span v-if="deal.country">in {{ deal.country.name }}</span>
      </h1>
      <div style="font-size: 0.8rem">
        <div v-if="!dealId">{{ deal }}</div>
        <!--        {{ deal.locations }}<br /><br />-->
        <!--        {{ deal.geojson }}-->
        <!--        {{ deal.datasources }}-->
      </div>
      <b-tabs
        id="tabNav"
        :key="dealId ? dealId + dealVersion : -1"
        content-class="mb-3"
        vertical
        pills
        nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
        nav-class="sticky-nav"
      >
        <b-tab
          :title="$t('Locations')"
          :active="active_tab === '#locations'"
          @click="updateRoute('#locations')"
        >
          <EditField
            v-model="deal.country"
            fieldname="country"
            :wrapper-classes="['row', 'my-3']"
            :label-classes="['col-md-3']"
            :value-classes="['col-md-9']"
            :disabled="deal.locations.length > 0"
          />
          <DealLocationsEditSection
            v-if="deal.country"
            :locations="deal.locations"
            :country="deal.country"
            :sections="deal_sections.general_info.subsections"
            :fields="deal_submodel_sections.location"
            @addEntry="addLocation"
            @removeEntry="removeLocation"
            @input="(newlocs) => (deal.locations = newlocs)"
          />
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
          @removeEntry="removeContract"
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
          title="Data sources"
          model-name="Data source"
          :entries="deal.datasources"
          :fields="deal_submodel_sections.datasource"
          model="datasource"
          :active="active_tab === '#data_sources'"
          @activated="updateRoute('#data_sources')"
          @addEntry="addDataSource"
          @removeEntry="removeDataSource"
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

      <div class="savebar-container">
        <div class="savebar">
          <button
            type="submit"
            class="btn btn-primary btn-sm mx-2"
            :disabled="saving_in_progress"
          >
            <span
              v-if="saving_in_progress"
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            ></span
            >&nbsp;
            {{ $t("Save") }}
          </button>
          {{ dealId ? $t("Saves your edits") : $t("Saves the deal as draft") }}
          <router-link
            v-if="dealId"
            class="btn btn-gray btn-sm mx-2"
            :to="{
              name: 'deal_detail',
              params: { dealId: deal.id, dealVersion: dealVersion },
            }"
          >
            {{ $t("Cancel save") }}
          </router-link>
          <a v-else class="btn btn-gray btn-sm mx-2" @click="$router.go(-1)">Cancel</a>
          <span>{{ $t("Leaves edit mode and forgets edits made") }}</span>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
  import DealEditSection from "$components/Deal/DealEditSection";
  import DealLocationsEditSection from "$components/Deal/DealLocationsEditSection";
  import DealSubmodelEditSection from "$components/Deal/DealSubmodelEditSection";
  import EditField from "$components/Fields/EditField";
  import { deal_gql_query } from "$store/queries";
  import gql from "graphql-tag";

  import { deal_sections, deal_submodel_sections } from "./deal_sections";

  export default {
    name: "DealEdit",
    components: {
      DealLocationsEditSection,
      EditField,
      DealSubmodelEditSection,
      DealEditSection,
    },
    props: {
      dealId: { type: [Number, String], required: false, default: null },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        deal: null,
        deal_sections,
        deal_submodel_sections,
        saving_in_progress: false,
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
        skip() {
          return !this.dealId;
        },
      },
    },
    computed: {
      active_tab() {
        return location.hash ? location.hash : "#locations";
      },
    },
    created() {
      if (!this.dealId) {
        this.deal = { country: null, locations: [], contracts: [], datasources: [] };
        // TODO: deleteme, just for development
        this.deal = {
          country: {
            id: 800,
            name: "Uganda",
            code_alpha2: "UG",
            point_lat_min: -1.469921875,
            point_lat_max: 4.22021484375,
            point_lon_min: 29.5619140625,
            point_lon_max: 34.9782226563,
          },
          locations: [],
          contracts: [],
          datasources: [],
        };
      }
    },
    methods: {
      updateRoute(emiter) {
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
      },
      deal_save() {
        this.saving_in_progress = true;
        this.$apollo
          .mutate({
            mutation: gql`
              mutation ($id: Int!, $version: Int, $payload: Payload) {
                deal_edit(id: $id, version: $version, payload: $payload) {
                  dealId
                  dealVersion
                }
              }
            `,
            variables: {
              id: this.dealId ? +this.dealId : -1,
              version: this.dealVersion ? +this.dealVersion : null,
              payload: { ...this.deal, versions: null, comments: null },
            },
          })
          .then((data) => {
            this.$router.push({
              name: "deal_detail",
              params: data.data.deal_edit,
            });
          })
          .catch((e) => {
            console.error({ e });
          });
      },
      addLocation(loc) {
        this.deal.locations.push(loc);
      },
      removeLocation(index) {
        if (confirm(this.$t("Do you really want to remove this location?")) === true) {
          this.deal.locations.splice(index, 1);
        }
      },
      addContract() {
        let maxid = 0;
        this.deal.contracts.forEach((l) => (maxid = Math.max(l.id, maxid)));
        this.deal.contracts.push(new Object({ id: maxid + 1 }));
      },
      addDataSource() {
        let maxid = 0;
        this.deal.datasources.forEach((l) => (maxid = Math.max(l.id, maxid)));
        this.deal.datasources.push(new Object({ id: maxid + 1 }));
      },
      removeContract(index) {
        if (confirm(this.$t("Do you really want to remove this contract?")) === true) {
          this.deal.contracts.splice(index, 1);
        }
      },
      removeDataSource(index) {
        if (
          confirm(this.$t("Do you really want to remove this data source?")) === true
        ) {
          this.deal.datasources.splice(index, 1);
        }
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

  .savebar-container {
    padding: 3em;

    .savebar {
      width: clamp(300px, auto, 800px);
      //height: 3rem;
      padding: 0.5rem;
      background-color: rgba(#dedede, 0.9);
      filter: drop-shadow(3px 3px 3px rgba(0, 0, 0, 0.3));
      position: fixed;
      right: 5px;
      bottom: 40px;
      display: grid;
      grid-template-columns: 2fr 5fr;
      gap: 5px 10px;
      border-radius: 5px;
      z-index: 1000;

      .btn {
        margin: 0 !important;
        font-size: 1.15em;
      }
      > span {
        align-self: center;
      }
    }
  }

  .btn-gray {
    background-color: #b1b1b1;
    &:hover {
      color: white;
      background-color: darken(#b1b1b1, 5%);
    }
  }
</style>
