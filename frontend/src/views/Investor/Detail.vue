<template>
  <div class="container investor-detail">
    <div v-if="!investor" class="row" style="height: 100%;">
      <LoadingPulse />
    </div>
    <div v-else class="row">
      <div class="col-sm-5 col-md-3">
        <h1>Investor #{{ investor.id }}</h1>
      </div>
      <div class="col-sm-7 col-md-9 panel-container">
        <a
          v-if="$store.getters.userAuthenticated"
          :href="`/legacy/investor/edit/${investor.id}/`"
          target="_blank"
        >
          <i class="fas fa-edit"></i> Edit
        </a>
        <div class="meta-panel">
          <DisplayField
            :wrapper_classes="['inlinefield']"
            :label_classes="['inlinelabel']"
            :value_classes="['inlineval']"
            fieldname="created_at"
            model="investor"
            :value="this.investor.created_at"
          />
          <DisplayField
            :wrapper_classes="['inlinefield']"
            :label_classes="['inlinelabel']"
            :value_classes="['inlineval']"
            fieldname="modified_at"
            model="investor"
            :value="this.investor.modified_at"
          />
        </div>
      </div>
    </div>
    <p v-if="not_public" class="alert alert-danger mb-4">{{ not_public }}</p>

    <div v-if="investor" class="row">
      <div class="col-xl-6 mb-3">
        <DisplayField
          :fieldname="fieldname"
          :readonly="true"
          v-model="investor[fieldname]"
          v-for="fieldname in fields"
          model="investor"
        />
      </div>
      <div
        class="col-lg-8 col-xl-6 mb-3"
        :class="{ loading_wrapper: !graphDataIsReady }"
        v-if="!investor_version"
      >
        <div v-if="!graphDataIsReady" style="height: 400px;">
          <LoadingPulse />
        </div>
        <InvestorGraph
          v-else
          :investor="investor"
          @newDepth="onNewDepth"
          :initDepth="depth"
        ></InvestorGraph>
      </div>
      <div
        v-else
        class="col-lg-8 col-xl-6 mb-3 d-flex justify-center align-items-center"
        style="color: #585858; background: #d4d4d4; border-radius: 5px;"
      >
        {{
          $t(
            "You're viewing an old version of this Investor, for which we don't have this diagram. To avoid confusion, it is deactivated here."
          )
        }}
      </div>
    </div>

    <b-tabs v-if="graphDataIsReady" content-class="mb-3">
      <b-tab>
        <template v-slot:title>
          <h5 v-html="`Involvements (${involvements.length})`"></h5>
        </template>
        <table class="table data-table">
          <thead>
            <tr>
              <th>Investor ID</th>
              <th>Name</th>
              <th>Country of registration</th>
              <th>Classification</th>
              <th>Relationship</th>
              <th>Ownership share</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="involvement in involvements">
              <td>
                <DisplayField
                  :wrapper_classes="['text-center']"
                  :value_classes="[]"
                  fieldname="id"
                  :value="involvement.investor.id"
                  model="investor"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="name"
                  :value="involvement.investor.name"
                  model="investor"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="country"
                  :value="involvement.investor.country"
                  model="investor"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="classification"
                  :value="involvement.investor.classification"
                  model="investor"
                  :show_label="false"
                />
              </td>
              <td>{{ detect_role(involvement) }}</td>
              <td>
                <span v-if="involvement.percentage">
                  {{ involvement.percentage }} %
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </b-tab>
      <b-tab v-if="'deals' in investor">
        <template v-slot:title>
          <h5
            v-html="
              `Deals (Involvements as Operating company) (${investor.deals.length})`
            "
          ></h5>
        </template>
        <table class="table data-table">
          <thead>
            <tr>
              <th>Deal ID</th>
              <th>Target country</th>
              <th>Intention of investment</th>
              <th>Current negotiation status</th>
              <th>Current implementation status</th>
              <th>Deal size</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="deal in deals">
              <td>
                <DisplayField
                  :wrapper_classes="['text-center']"
                  :value_classes="[]"
                  fieldname="id"
                  :value="deal.id"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="country"
                  :value="deal.country"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="current_intention_of_investment"
                  :value="deal.current_intention_of_investment"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="current_negotiation_status"
                  :value="deal.current_negotiation_status"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="current_implementation_status"
                  :value="deal.current_implementation_status"
                  :show_label="false"
                />
              </td>
              <td>
                <DisplayField
                  :wrapper_classes="[]"
                  :value_classes="[]"
                  fieldname="deal_size"
                  :value="deal.deal_size"
                  :show_label="false"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </b-tab>
      <b-tab>
        <template v-slot:title>
          <h5>{{ $t("Investor History") }}</h5>
        </template>
        <InvestorHistory
          :investor="investor"
          :investor_id="investor_id"
          :investor_version="investor_version"
        />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import store from "/store";
  import { mapState } from "vuex";
  import InvestorGraph from "/components/Investor/InvestorGraph";
  import DisplayField from "/components/Fields/DisplayField";
  import LoadingPulse from "/components/Data/LoadingPulse";
  import InvestorHistory from "../../components/Investor/InvestorHistory";
  import { investor_query } from "../../store/queries";

  export default {
    name: "InvestorDetail",
    components: { InvestorHistory, LoadingPulse, InvestorGraph, DisplayField },
    props: ["investor_id", "investor_version"],
    data() {
      return {
        investor: null,
        fields: [
          "name",
          "country",
          "classification",
          "homepage",
          "opencorporates",
          "comment",
        ],
        depth: 0,
        includeDealsInQuery: false,
      };
    },
    apollo: { investor: investor_query },
    computed: {
      ...mapState({
        formFields: (state) => state.formfields,
      }),
      involvements() {
        return this.investor.involvements || [];
      },
      not_public() {
        if (this.investor) {
          if (this.investor.status === 1 || this.investor.status === 6)
            return this.$t("This investor version is pending.");
          if (this.investor.status === 4)
            return this.$t(
              "This investor has been deleted. It is not visible for public users."
            );
          if (this.investor.status === 5)
            return this.$t(
              "This investor version has been rejected. It is not visible for public users."
            );
        }
        return null;
      },
      deals() {
        if ("deals" in this.investor) {
          return this.investor.deals.sort((a, b) => {
            return a.id - b.id;
          });
        } else return [];
      },
      graphDataIsReady() {
        return (
          this.investor &&
          "involvements" in this.investor &&
          this.investor &&
          "deals" in this.investor &&
          !this.$apollo.queries.investor.loading
        );
      },
      tableDataIsReady() {
        return (
          this.investor &&
          "involvements" in this.investor &&
          this.investor &&
          "deals" in this.investor
        );
      },
    },
    methods: {
      detect_role(investor) {
        if (investor.role === "PARENT") {
          if (investor.involvement_type === "INVESTOR") return "Parent company";
          if (investor.involvement_type === "VENTURE")
            return "Involved in as Parent Company";
        }
        if (investor.role === "LENDER") {
          if (investor.involvement_type === "INVESTOR")
            return "Tertiary investor/lender";
          if (investor.involvement_type === "VENTURE")
            return "Involved in as Tertiary investor/lender";
        }
      },
      onNewDepth(value) {
        if (value > this.depth) {
          this.depth = +value;
        }
      },
    },
    watch: {
      investor_id(investor_id, oldInvestorId) {
        if (investor_id !== oldInvestorId) {
          this.includeDealsInQuery = false;
        }
      },
      investor(investor, oldInvestor) {
        if (!oldInvestor) {
          // initial load complete, also load deals
          this.includeDealsInQuery = true;
          this.depth = 1;
        }
        let title = `${investor.name} <small>(#${investor.id})</small>`;
        store.dispatch("setPageContext", {
          title,
          breadcrumbs: [
            { link: { name: "wagtail" }, name: "Home" },
            { link: { name: "list_investors" }, name: "Data" },
            { name: `Investor #${investor.id}` },
          ],
        });
      },
    },
  };
</script>

<style lang="scss">
  @import "src/scss/colors";

  .investor-detail {
    h1 {
      color: $lm_dark;
      text-align: left;
      text-transform: none;

      &:before {
        display: none;
      }
    }
  }
</style>
