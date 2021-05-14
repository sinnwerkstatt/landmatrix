<template>
  <div v-if="investor" class="container investor-edit">
    <b-tabs
      id="tabNav"
      :key="investorId + investorVersion"
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
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import { investor_query } from "$store/queries";
  import EditField from "$components/Fields/EditField";
  import InvolvementEdit from "$components/Investor/InvolvementEdit";

  export default {
    name: "InvestorEdit",
    components: { InvolvementEdit, EditField },
    props: {
      investorId: { type: [Number, String], required: true },
      investorVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        investor: null,
        includeDealsInQuery: false,
        involvementsIncludeVentures: false,
        depth: 1,
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
    apollo: { investor: investor_query },

    computed: {
      active_tab() {
        return location.hash ? location.hash : "#general";
      },
      parents() {
        return this.investor.involvements
          .filter((i) => i.role === "PARENT")
          .sort((a, b) => a.id - b.id);
      },
      lenders() {
        return this.investor.involvements
          .filter((i) => i.role === "LENDER")
          .sort((a, b) => a.id - b.id);
      },
    },
    methods: {
      updateRoute(emiter) {
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
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
