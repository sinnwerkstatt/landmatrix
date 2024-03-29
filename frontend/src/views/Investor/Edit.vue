<template>
  <div>
    <div v-if="investor" class="container investor-edit">
      <div class="investor-edit-heading">
        <h1>
          {{
            investorId
              ? $t("Editing Investor #") + investorId
              : $t("Adding new investor")
          }}
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
          <button class="btn btn-secondary btn-sm mx-2" @click="quitEditor(false)">
            {{ $t("Close") }}
          </button>

          <span>{{ $t("Leave edit mode") }}</span>
        </div>
      </div>

      <div class="investor-edit-nav">
        <ul>
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

      <div class="investor-edit-content">
        <section v-if="active_tab === '#general'">
          <form id="general">
            <div class="container">
              <EditField
                v-for="fieldname in general_fields"
                :key="fieldname"
                v-model="investor[fieldname]"
                :fieldname="fieldname"
                :label-classes="['col-md-3']"
                :value-classes="['col-md-9']"
                :wrapper-classes="['row', 'my-3']"
                model="investor"
              />
            </div>
          </form>
        </section>

        <InvestorSubmodelEditSection
          v-if="active_tab === '#parents'"
          id="parents"
          :entries="parents"
          model-name="Parent company"
          title="Parent companies"
          @addEntry="addInvestor('PARENT')"
          @removeEntry="removeInvestor"
        />

        <InvestorSubmodelEditSection
          v-if="active_tab === '#tertiaries'"
          id="tertiaries"
          :entries="lenders"
          model-name="Tertiary investor/lender"
          title="Tertiary investors/lenders"
          @addEntry="addInvestor('LENDER')"
          @removeEntry="removeInvestor"
        />
      </div>
    </div>
    <div v-else>
      <LoadingPulse />
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

<script lang="ts">
  import LoadingPulse from "$components/Data/LoadingPulse";
  import InvestorSubmodelEditSection from "$components/Deal/InvestorSubmodelEditSection";
  import EditField from "$components/Fields/EditField";
  import Overlay from "$components/Overlay";
  import { investor_edit_query } from "$store/queries";
  import gql from "graphql-tag";
  import Vue from "vue";

  export default Vue.extend({
    name: "InvestorEdit",
    components: {
      InvestorSubmodelEditSection,
      Overlay,
      LoadingPulse,
      EditField,
    },

    beforeRouteEnter(to, from, next) {
      next((vm) => {
        console.log("Investor edit: Route enter");
        vm.active_tab = to.hash || "#general";
      });
    },
    beforeRouteUpdate(to, from, next) {
      console.log("Investor edit: Route update");
      if (to.hash) this.active_tab = to.hash;
      next();
    },
    props: {
      investorId: { type: [Number, String], required: false, default: null },
      investorVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        investor: null,
        original_investor: "",
        saving_in_progress: false,
        show_really_quit_overlay: false,
        active_tab: "#general",
        tabs: {
          general: this.$t("General"),
          parents: this.$t("Parent companies"),
          tertiaries: this.$t("Tertiary investors/lenders"),
        },
        general_fields: [
          "name",
          "country",
          "classification",
          "homepage",
          "opencorporates",
          "comment",
        ],
      };
    },
    apollo: {
      investor: {
        query: investor_edit_query,
        variables() {
          return { id: +this.investorId, version: +this.investorVersion };
        },
        update({ investor }) {
          this.original_investor = JSON.stringify(investor);
          return investor;
        },
        skip() {
          return !this.investorId;
        },
        fetchPolicy: "no-cache",
      },
    },

    computed: {
      parents() {
        return this.investor.investors
          ?.filter((i) => i.role === "PARENT")
          .sort((a, b) => a.id - b.id);
      },
      lenders() {
        return this.investor.investors
          ?.filter((i) => i.role === "LENDER")
          .sort((a, b) => a.id - b.id);
      },
      current_form() {
        return document.querySelector(this.active_tab);
      },
      form_changed() {
        return JSON.stringify(this.investor) !== this.original_investor;
      },
    },
    created() {
      if (!this.investorId) {
        this.investor = { investors: [] };
        this.original_investor = JSON.stringify(this.investor);
      }
    },
    methods: {
      quitEditor(force) {
        if (this.form_changed && !force) this.show_really_quit_overlay = true;
        else if (!this.investorId) this.$router.push("/");
        else
          this.$router.push({
            name: "investor_detail",
            params: {
              investorId: this.investorId,
              investorVersion: this.investorVersion,
            },
          });
      },
      saveButtonPressed() {
        this.investor_save(location.hash);
      },
      updateRoute(hash) {
        if (location.hash === hash) return;
        if (!this.form_changed) this.$router.push({ hash });
        else this.investor_save(hash);
      },
      investor_save(hash) {
        if (!this.current_form.checkValidity()) {
          this.current_form.reportValidity();
          return;
        }

        this.saving_in_progress = true;
        let payload = {
          ...this.investor,
          versions: null,
          comments: null,
          workflowinfos: null,
        };
        payload.investors = payload.investors.map((i) => {
          if (i.id?.toString().startsWith("new")) delete i.id;
          return i;
        });
        return this.$apollo
          .mutate({
            mutation: gql`
              mutation ($id: Int!, $version: Int, $payload: Payload) {
                investor_edit(id: $id, version: $version, payload: $payload) {
                  investorId
                  investorVersion
                }
              }
            `,
            variables: {
              id: this.investorId ? +this.investorId : -1,
              version: this.investorVersion ? +this.investorVersion : null,
              payload,
            },
          })
          .then(({ data: { investor_edit } }) => {
            this.original_investor = JSON.stringify(this.investor);

            this.saving_in_progress = false;
            if (
              location.hash !== hash ||
              +this.investorVersion !== +investor_edit.investorVersion
            )
              this.$router.push({ name: "investor_edit", params: investor_edit, hash });
          });
      },
      addInvestor(role) {
        if (!this.current_form.checkValidity()) this.current_form.reportValidity();
        else {
          // this is a somewhat dirty hack to add more investors and still list them correctly
          let id = `new` + Math.random().toString().substring(10);
          this.investor.investors.push({ role, id });
        }
      },
      removeInvestor(id) {
        let message = this.$t("Do you really want to remove the involvement?");
        this.$bvModal
          .msgBoxConfirm(message, {
            size: "sm",
            okTitle: this.$t("Delete"),
            cancelTitle: this.$t("Cancel"),
            centered: true,
          })
          .then((confirmed) => {
            if (confirmed)
              this.investor.investors = this.investor.investors.filter(
                (i) => i.id !== id
              );
          });
      },
    },
  });
</script>

<style lang="scss">
  .investor-edit {
    overflow: hidden;
    height: calc(100vh - 60px - 31px);
    width: 100vw;
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: 2.5rem auto;
  }

  .investor-edit-heading {
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

  .investor-edit-nav {
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

    ul {
      list-style: none;
      padding-left: 0;

      li {
        cursor: pointer;
        padding: 0.5rem 1rem 0.5rem 0;
        border-right: 1px solid var(--color-lm-orange);
        color: var(--color-lm-orange);
        border-radius: 0;

        &.active {
          border-right-width: 3px;
          background-color: inherit;
          color: var(--color-lm-dark);

          a {
            color: var(--color-lm-dark);
          }
        }
      }
    }
  }

  .investor-edit-content {
    height: 100%;
    grid-column: span 9;
    overflow-y: auto;
  }
</style>
