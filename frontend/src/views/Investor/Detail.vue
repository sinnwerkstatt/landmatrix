<template>
  <div>
    <div class="loadingscreen" v-if="!investor">
      <div class="loader"></div>
    </div>
    <div class="container" v-if="investor"></div>
    <div class="container" v-if="investor">
      <h2>General Info</h2>
      <div class="row">
        <div class="col-xl-6 mb-3">
          <Field
            :fieldname="fieldname"
            :readonly="true"
            v-model="investor[fieldname]"
            v-for="fieldname in fields"
            model="investor"
          />
        </div>
        <div
          class="col-lg-8 col-xl-6 mb-3"
          :class="{ loading_wrapper: !involvements.length }"
        >
          <InvestorGraph
            v-if="involvements.length"
            :investor="investor"
          ></InvestorGraph>
          <div v-else class="loader" style="height: 400px;"></div>
        </div>
      </div>

      <b-tabs content-class="mb-3">
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
                <td v-html="investorValue(involvement, 'id')"></td>
                <td v-html="investorValue(involvement.investor, 'name')"></td>
                <td v-html="investorValue(involvement.investor, 'country')"></td>
                <td v-html="investorValue(involvement.investor, 'classification')"></td>
                <td>{{ detect_role(involvement) }}</td>
                <td>{{ involvement.percentage }}</td>
              </tr>
            </tbody>
          </table>
        </b-tab>
        <b-tab>
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
  </div>
</template>

<script>
  import store from "/store";
  import gql from "graphql-tag";
  import { mapState } from "vuex";
  import { getDealValue, getInvestorValue } from "/components/Data/table_mappings";
  import InvestorGraph from "/components/Investor/InvestorGraph";
  import Field from "/components/Fields/Field";

  let investor_query = gql`
    query Investor($investorID: Int!, $depth: Int) {
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
        deals {
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
    components: { InvestorGraph, Field },
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
      };
    },
    apollo: {
      investor() {
        return {
          query: investor_query,
          variables: {
            investorID: +this.investor_id,
            depth: 0,
          },
        };
      },
    },
    computed: {
      ...mapState({
        investor_fields: (state) => state.investor.investor_fields,
      }),
      involvements() {
        return this.investor.involvements || [];
      },
      deals() {
        return this.investor.deals.sort((a,b) => { return a.id - b.id;})
      }
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
      }
    },
    mounted() {
      this.$apollo.addSmartQuery("investor", {
        query: investor_query,
        variables: {
          investorID: +this.investor_id,
          depth: 3,
        },
      });
    },
    watch: {
      investor(investor, oldInvestor) {
        let title = `${investor.name} <small>(#${investor.id})</small>`;
        store.dispatch("setPageContext", {
          title,
          breadcrumbs: [
            { link: { name: "wagtail" }, name: "Home" },
            { link: { name: "investor_list" }, name: "Data" },
            { name: `Investor #${investor.id}` },
          ],
        });
      },
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";
  .loading_wrapper {
    background: grey;
    width: 100%;
    min-height: 250px;
    color: $lm_orange;
  }
</style>
