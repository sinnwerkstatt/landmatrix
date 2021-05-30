<template>
  <div class="container investor-edit">
    <h1>
      {{ investor.name }}
    </h1>
    {{ investor }}
    <form @submit="submitInvestor">
      <b-tabs
        id="tabNav"
        :key="investorId ? investorId + investorVersion : -1"
        content-class="mb-3"
        vertical
        pills
        nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
        nav-class="sticky-nav"
      >
        <b-tab
          :title="$t('General')"
          :active="active_tab === '#general'"
          @click="updateRoute('#general')"
        >
          <EditField
            v-for="fieldname in general_fields"
            :key="fieldname"
            v-model="investor[fieldname]"
            model="investor"
            :fieldname="fieldname"
            :label-classes="['display-field-value', 'col-md-3']"
            :value-classes="['display-field-label', 'col-md-9']"
          />
        </b-tab>
        <b-tab
          :title="$t('Parent companies')"
          :active="active_tab === '#parents'"
          @click="updateRoute('#parents')"
        >
          <div v-for="(parent, i) in parents" :key="parent.id">
            <h3>
              {{ $t("Parent company") }} <small>#{{ i + 1 }}</small>
            </h3>
            <InvolvementEdit :involvement="parent"></InvolvementEdit>
          </div>
          <button type="button" class="btn btn-primary" @click="addInvestor('PARENT')">
            <i class="fa fa-plus"></i> {{ $t("Add parent company") }}
          </button>
        </b-tab>

        <b-tab
          :title="$t('Tertiary investors/lenders')"
          :active="active_tab === '#tertiary'"
          @click="updateRoute('#tertiary')"
        >
          <div v-for="(lender, i) in lenders" :key="lender.id">
            <h3>
              {{ $t("Tertiary investor/lender") }} <small>#{{ i + 1 }}</small>
            </h3>
            <InvolvementEdit :involvement="lender" type="lender"></InvolvementEdit>
          </div>
          <button type="button" class="btn btn-primary" @click="addInvestor('LENDER')">
            <i class="fa fa-plus"></i> {{ $t("Add tertiary investor/lender") }}
          </button>
        </b-tab>
      </b-tabs>

      <div class="savebar">
        <button class="btn btn-primary">Save</button>
      </div>
    </form>
  </div>
</template>

<script>
  import EditField from "$components/Fields/EditField";
  import InvolvementEdit from "$components/Investor/InvolvementEdit";
  import { investor_edit_query } from "$store/queries";

  export default {
    name: "InvestorEdit",
    components: { InvolvementEdit, EditField },
    props: {
      investorId: { type: [Number, String], required: false, default: null },
      investorVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        investor: null,
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
    apollo: { investor: investor_edit_query },

    computed: {
      active_tab() {
        return location.hash ? location.hash : "#general";
      },
      parents() {
        return this.investor.investors
          .filter((i) => i.role === "PARENT")
          .sort((a, b) => a.id - b.id);
      },
      lenders() {
        return this.investor.investors
          .filter((i) => i.role === "LENDER")
          .sort((a, b) => a.id - b.id);
      },
    },
    created() {
      if (!this.investorId) {
        this.investor = { investors: [] };
      }
      if (this.$route.query.newName) {
        this.investor.name = this.$route.query.newName;
      }
    },
    methods: {
      updateRoute(emiter) {
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
      },
      addInvestor(role) {
        this.investor.investors.push({ role });
      },
      submitInvestor() {
        if (this.$route.query.newName) {
          window.close("juchu!");
        }
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

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
</style>
