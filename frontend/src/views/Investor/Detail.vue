<template>
  <div>
    <div class="loadingscreen" v-if="!investor">
      <div class="loader"></div>
    </div>
    <div class="container" v-if="investor"></div>
    <div class="container" v-if="investor">
      <h2>General Info</h2>
      <div class="row">
        <div class="col">
          <Field
            :formfield="formfield"
            :readonly="true"
            v-model="investor[formfield.name]"
            v-for="formfield in investor_fields.general_info.fields"
          />
        </div>
        <div class="col" :class="{ loading_wrapper: !involvements.length }">
          <InvestorGraph
            v-if="involvements.length"
            :investor="investor"
          ></InvestorGraph>
          <div v-else class="loader"></div>
        </div>
      </div>

      <b-tabs content-class="mt-3">
        <b-tab :title="`Involvements (${involvements.length})`">
          <table class="table">
            <thead>
              <tr>
                <th>Investor ID</th>
                <th>Name</th>
                <th>Country</th>
                <th>Classification</th>
                <th>Relationship</th>
                <th>Ownership share</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="involvement in involvements">
                <td>
                  <router-link
                    :to="{
                      name: 'investor_detail',
                      params: { investor_id: involvement.investor.id },
                    }"
                    v-slot="{ href }"
                  >
                    <a :href="href">#{{ involvement.investor.id }}</a>
                  </router-link>
                </td>
                <td>{{ involvement.investor.name }}</td>
                <td>{{ involvement.investor.country.name }}</td>
                <td>{{ involvement.investor.classification }}</td>
                <td>{{ detect_role(involvement) }}</td>
                <td>{{ involvement.percentage }}</td>
              </tr>
            </tbody>
          </table>
        </b-tab>
        <b-tab
          :title="`Deals (Involvements as Operating company) (${investor.deals.length})`"
        >
          <table class="table">
            <thead>
              <tr>
                <th>Deal ID</th>
                <th>Country</th>
                <th>Classification</th>
                <th>Relationship</th>
                <th>Ownership share</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="deal in investor.deals">
                <td>
                  <router-link
                    :to="{
                      name: 'deal_detail',
                      params: { deal_id: deal.id },
                    }"
                    v-slot="{ href }"
                  >
                    <a :href="href">#{{ deal.id }}</a>
                  </router-link>
                </td>
                <td>{{ deal.country.name }}</td>
                <td>{{ deal }}</td>
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
            name
          }
        }
        involvements(depth: $depth)
      }
    }
  `;

  export default {
    name: "InvestorDetail",
    components: { InvestorGraph, Field },
    props: ["investor_id"],
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
    data() {
      return {
        investor: null,
        fields: {
          name: "Name",
          country: "Country of registration/origin",
          classification: "Classification",
          homepage: "Homepage",
          opencorporates: "Opencorporates link",
          comment: "Comment",
        },
      };
    },
    computed: {
      ...mapState({
        investor_fields: (state) => state.investor.investor_fields,
      }),
      involvements() {
        return this.investor.involvements || [];
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
    },
    mounted() {
      this.$apollo.addSmartQuery("investor", {
        query: investor_query,
        variables: {
          investorID: +this.investor_id,
          depth: 4,
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

<style>
  .loading_wrapper {
    background: grey;
    width: 100%;
    height: 100%;
  }
</style>
