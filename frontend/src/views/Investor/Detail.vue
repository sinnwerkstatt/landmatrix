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
              <td v-html="investorValue(involvement.investor, 'id')"></td>
              <td v-html="investorValue(involvement.investor, 'name')"></td>
              <td v-html="investorValue(involvement.investor, 'country')"></td>
              <td v-html="investorValue(involvement.investor, 'classification')"></td>
              <td>{{ detect_role(involvement) }}</td>
              <td>{{ involvement.percentage }}</td>
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
              <td v-html="dealValue(deal, 'id')"></td>
              <td v-html="dealValue(deal, 'country')"></td>
              <td v-html="dealValue(deal, 'intention_of_investment')"></td>
              <td v-html="dealValue(deal, 'current_negotiation_status')"></td>
              <td v-html="dealValue(deal, 'current_implementation_status')"></td>
              <td v-html="dealValue(deal, 'deal_size')"></td>
            </tr>
          </tbody>
        </table>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import store from "/store";
  import gql from "graphql-tag";
  import { mapState } from "vuex";
  import { getDealValue, getInvestorValue } from "/components/Data/table_mappings";
  import InvestorGraph from "/components/Investor/InvestorGraph";
  import DisplayField from "/components/Fields/DisplayField";
  import LoadingPulse from "/components/Data/LoadingPulse";

  let investor_query = gql`
    query Investor($investorID: Int!, $depth: Int, $includeDeals: Boolean!) {
      investor(id: $investorID) {
        id
        name
        country {
          id
          name
        }
        classification
        homepage
        opencorporates
        comment
        # involvements
        status
        created_at
        modified_at
        deals @include(if: $includeDeals) {
          id
          country {
            id
          }
          recognition_status
          nature_of_deal
          intention_of_investment
          negotiation_status
          implementation_status
          current_intention_of_investment
          current_negotiation_status
          current_implementation_status
          deal_size
        }
        involvements(depth: $depth)
      }
    }
  `;

  export default {
    name: "InvestorDetail",
    components: { LoadingPulse, InvestorGraph, DisplayField },
    props: ["investor_id"],
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
    apollo: {
      investor: {
        query: investor_query,
        variables() {
          return {
            investorID: +this.investor_id,
            depth: this.depth,
            includeDeals: this.includeDealsInQuery,
          };
        },
        update(data) {
          if (!data.investor) {
            this.$router.push({
              name: "404",
              params: [this.$router.currentRoute.path],
              replace: true,
            });
          }
          return data.investor;
        },
      },
    },
    computed: {
      ...mapState({
        investor_fields: (state) => state.investor.investor_fields,
        formFields: (state) => state.formfields,
      }),
      involvements() {
        return this.investor.involvements || [];
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
      investorValue(investor, fieldName) {
        return getInvestorValue(this, investor, fieldName);
      },
      dealValue(deal, fieldName) {
        return getDealValue(this, deal, fieldName);
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
  @import "../../scss/colors";

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
