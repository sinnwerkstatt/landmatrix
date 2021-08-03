<template>
  <div>
    <div v-if="deal" class="container deal-edit">
      <div class="deal-edit-heading">
        <h1>
          {{ dealId ? $t("Editing Deal #") + dealId : $t("Adding new deal") }}
          <span v-if="deal.country">{{ $t("in") }} {{ deal.country.name }}</span>
        </h1>

        <div class="savebar-container">
          <button
            :disabled="!form_changed || saving_in_progress"
            class="btn btn-primary btn-sm mx-2"
            type="submit"
            @click="saveButtonPressed"
          >
            <span
              v-if="saving_in_progress"
              aria-hidden="true"
              class="spinner-border spinner-border-sm"
              role="status"
            ></span>
            &nbsp;
            {{ $t("Save") }}
          </button>
          <button
            v-if="dealId"
            class="btn btn-secondary btn-sm mx-2"
            @click="quitEditor(false)"
          >
            {{ $t("Close") }}
          </button>
          <a v-else class="btn btn-gray btn-sm mx-2" @click="$router.go(-1)">
            {{ $t("Cancel") }}
          </a>
          <span>{{ $t("Leaves edit mode") }}</span>
        </div>
      </div>
      <div class="deal-edit-nav">
        <ul class="lm-nav">
          <li
            v-for="(tabname, tabid) in tabs"
            :key="tabid"
            :class="{ active: active_tab === `#${tabid}` }"
          >
            <a :href="`#${tabid}`" @click.prevent="updateRoute(`#${tabid}`)">
              {{ tabname }}
            </a>
          </li>
        </ul>
      </div>
      <div class="deal-edit-content">
        <section v-if="active_tab === '#locations'">
          <form id="locations">
            <div class="container">
              <EditField
                v-model="deal.country"
                :disabled="deal.locations.length > 0"
                :label-classes="['col-md-3']"
                :value-classes="['col-md-9']"
                :wrapper-classes="['row', 'my-3']"
                fieldname="country"
              />
            </div>
            <DealLocationsEditSection
              v-if="deal.country"
              :country="deal.country"
              :fields="deal_submodel_sections.location"
              :locations="deal.locations"
              :sections="deal_sections.general_info.subsections"
              @input="(newlocs) => (deal.locations = newlocs)"
            />
          </form>
        </section>

        <DealEditSection
          v-if="active_tab === '#general'"
          id="general"
          :deal="deal"
          :sections="deal_sections.general_info.subsections"
          :title="deal_sections.general_info.label"
        />
        <DealSubmodelEditSection
          v-if="active_tab === '#contracts'"
          id="contracts"
          :entries="deal.contracts"
          :fields="deal_submodel_sections.contract"
          model="contract"
          model-name="Contract"
          title="Contracts"
          @addEntry="addContract"
          @removeEntry="removeContract"
        />

        <DealEditSection
          v-if="active_tab === '#employment'"
          id="employment"
          :deal="deal"
          :sections="deal_sections.employment.subsections"
          :title="deal_sections.employment.label"
        />

        <DealEditSection
          v-if="active_tab === '#investor_info'"
          id="investor_info"
          :deal="deal"
          :sections="deal_sections.investor_info.subsections"
          :title="deal_sections.investor_info.label"
        />

        <DealSubmodelEditSection
          v-if="active_tab === '#data_sources'"
          id="data_sources"
          :entries="deal.datasources"
          :fields="deal_submodel_sections.datasource"
          model="datasource"
          model-name="Data source"
          title="Data sources"
          @addEntry="addDataSource"
          @removeEntry="removeDataSource"
        />

        <DealEditSection
          v-if="active_tab === '#local_communities'"
          id="local_communities"
          :deal="deal"
          :sections="deal_sections.local_communities.subsections"
          :title="deal_sections.local_communities.label"
        />

        <DealEditSection
          v-if="active_tab === '#former_use'"
          id="former_use"
          :deal="deal"
          :sections="deal_sections.former_use.subsections"
          :title="deal_sections.former_use.label"
        />

        <DealEditSection
          v-if="active_tab === '#produce_info'"
          id="produce_info"
          :deal="deal"
          :sections="deal_sections.produce_info.subsections"
          :title="deal_sections.produce_info.label"
        />

        <DealEditSection
          v-if="active_tab === '#water'"
          id="water"
          :deal="deal"
          :sections="deal_sections.water.subsections"
          :title="deal_sections.water.label"
        />

        <DealEditSection
          v-if="active_tab === '#gender_related_info'"
          id="gender_related_info"
          :deal="deal"
          :sections="deal_sections.gender_related_info.subsections"
          :title="deal_sections.gender_related_info.label"
        />

        <DealEditSection
          v-if="active_tab === '#guidelines_and_principles'"
          id="guidelines_and_principles"
          :deal="deal"
          :sections="deal_sections.guidelines_and_principles.subsections"
          :title="deal_sections.guidelines_and_principles.label"
        />

        <DealEditSection
          v-if="active_tab === '#overall_comment'"
          id="overall_comment"
          :deal="deal"
          :sections="deal_sections.overall_comment.subsections"
          :title="deal_sections.overall_comment.label"
        />
      </div>
    </div>
    <div v-else>
      <LoadingPulse></LoadingPulse>
    </div>
    <Overlay
      v-if="show_really_quit_overlay"
      :title="$t('Quit edit mode')"
      @cancel="show_really_quit_overlay = false"
      @submit="quitEditor(true)"
    >
      You have unsaved changes. Are you sure you want to exit the edit mode?
    </Overlay>
  </div>
</template>

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";
  import DealEditSection from "$components/Deal/DealEditSection";
  import DealLocationsEditSection from "$components/Deal/DealLocationsEditSection";
  import DealSubmodelEditSection from "$components/Deal/DealSubmodelEditSection";
  import EditField from "$components/Fields/EditField";
  import Overlay from "$components/Overlay";
  import { deal_gql_query } from "$store/queries";
  import { removeEmptyEntries } from "$utils";
  import gql from "graphql-tag";

  import { deal_sections, deal_submodel_sections } from "./deal_sections";

  export default {
    name: "DealEdit",
    components: {
      Overlay,
      LoadingPulse,
      DealLocationsEditSection,
      EditField,
      DealSubmodelEditSection,
      DealEditSection,
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        console.log("Deal edit: Route enter");
        vm.updatePageContext(to);
        if (!to.hash) {
          vm.active_tab = "#locations";
        }
      });
    },
    beforeRouteUpdate(to, from, next) {
      console.log("Deal edit: Route update");
      this.updatePageContext(to);
      next();
    },
    props: {
      dealId: { type: [Number, String], required: false, default: null },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        original_deal: null,
        deal: null,
        deal_sections,
        deal_submodel_sections,
        saving_in_progress: false,
        show_really_quit_overlay: false,
        active_tab: "#locations",
        tabs: {
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
          guidelines_and_principles: this.$t("Guidelines & Principles"),
          overall_comment: this.$t("Overall comment"),
        },
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
          this.original_deal = JSON.stringify(data.deal);
          return data.deal;
        },
        skip() {
          return !this.dealId;
        },
        fetchPolicy: "no-cache",
      },
    },
    computed: {
      get_save_description() {
        if (!this.dealId) {
          // deal add
          return this.$t("Saves the deal as draft");
        } else {
          if (this.deal && this.deal.draft_status === 1) {
            // new drafts
            return this.$t("Updates the existing draft version");
          } else {
            return this.$t("Saves a new draft version of the deal");
          }
        }
      },
      current_form() {
        return document.querySelector(this.active_tab);
      },
      form_changed() {
        return JSON.stringify(this.deal) !== this.original_deal;
      },
    },
    created() {
      if (!this.dealId) {
        this.deal = { country: null, locations: [], contracts: [], datasources: [] };
        this.original_deal = JSON.stringify(this.deal);
      }
    },
    methods: {
      quitEditor(force) {
        if (this.form_changed && !force) this.show_really_quit_overlay = true;
        else if (!this.dealId) this.$router.push("/");
        else
          this.$router.push({
            name: "deal_detail",
            params: { dealId: this.dealId, dealVersion: this.dealVersion },
          });
      },
      saveButtonPressed() {
        if (!this.current_form.checkValidity()) this.current_form.reportValidity();
        else this.deal_save(location.hash);
      },
      updateRoute(hash) {
        if (location.hash === hash) return;
        if (!this.form_changed) {
          this.$router.push({ hash });
          return;
        }

        if (!this.current_form.checkValidity()) this.current_form.reportValidity();
        else this.deal_save(hash);
      },

      updatePageContext(to) {
        if (to.hash) {
          // only update if hash is present (otherwise #locations are active by default)
          this.active_tab = to.hash;
        }
      },
      deal_save(hash) {
        this.saving_in_progress = true;
        this.deal.locations = removeEmptyEntries(this.deal.locations);
        this.deal.contracts = removeEmptyEntries(this.deal.contracts);
        this.deal.datasources = removeEmptyEntries(this.deal.datasources);
        return this.$apollo
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
              payload: {
                ...this.deal,
                versions: null,
                comments: null,
                workflowinfos: null,
              },
            },
          })
          .then(({ data: { deal_edit } }) => {
            this.original_deal = JSON.stringify(this.deal);
            this.saving_in_progress = false;
            if (location.hash !== hash || this.dealVersion !== deal_edit.dealVersion)
              this.$router.push({ name: "deal_edit", params: deal_edit, hash });
          });
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
        this.removeSubmodelEntry(this.deal.contracts, index, "contract");
      },
      removeDataSource(index) {
        this.removeSubmodelEntry(this.deal.datasources, index, "data source");
      },
      removeSubmodelEntry(submodels, index, label) {
        let message =
          this.$t("Do you really want to remove " + label) + ` #${index + 1}?`;
        this.$bvModal
          .msgBoxConfirm(message, {
            size: "sm",
            okTitle: this.$t("Delete"),
            cancelTitle: this.$t("Cancel"),
            centered: true,
          })
          .then((confirmed) => {
            if (confirmed) {
              submodels.splice(index, 1);
            }
          });
      },
    },
  };
</script>

<style lang="scss">
  .deal-edit {
    overflow: hidden;
    height: calc(100vh - 60px - 31px);
    width: 100vw;
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: 2.5rem auto;
  }

  .deal-edit-heading {
    grid-column: span 12;
    display: flex;

    h1 {
      color: var(--color-lm-dark);
      text-align: left;
      text-transform: none;

      &:before {
        display: none;
      }
    }
  }

  .deal-edit-nav {
    grid-column: span 3;
    height: 100%;
    width: 100%;
    overflow-y: auto;
    padding: 0 1rem 0 0;

    &::-webkit-scrollbar {
      display: none;
    }

    -ms-overflow-style: none; /* IE and Edge */
    //noinspection CssUnknownProperty
    scrollbar-width: none; /* Firefox */
  }

  .deal-edit-content {
    height: 100%;
    grid-column: span 9;
    overflow-y: auto;
  }
</style>
