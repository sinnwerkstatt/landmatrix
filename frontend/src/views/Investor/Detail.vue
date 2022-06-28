<template>
  <div v-if="investor">
    <InvestorManageHeader
      v-if="userAuthenticated"
      :investor="investor"
      :investor-version="investorVersion"
      @change_status="changeStatus"
      @delete="deleteInvestor"
      @copy="copyInvestor"
      @reload="reloadInvestor"
    />
    <div v-else class="container investor-detail">
      <div class="row">
        <div>
          <h1>
            {{ investor.name }} <small>#{{ investor.id }}</small>
          </h1>
        </div>
        <div class="panel-container ml-auto">
          <HeaderDates :obj="investor" />
        </div>
      </div>
    </div>

    <div class="container investor-detail">
      <div class="row">
        <div class="col-xl-6 mb-3">
          <DisplayField
            v-for="fieldname in fields"
            :key="fieldname"
            v-model="investor[fieldname]"
            :fieldname="fieldname"
            :readonly="true"
            model="investor"
          />
        </div>
        <div
          v-if="!investorVersion"
          :class="{ loading_wrapper: !graphDataIsReady }"
          class="col-lg-8 col-xl-6 mb-3"
        >
          <div v-if="!graphDataIsReady" style="height: 400px">
            <LoadingPulse />
          </div>
          <InvestorGraph
            v-else
            :init-depth="depth"
            :investor="investor"
            @newDepth="onNewDepth"
          />
        </div>
        <div
          v-else
          class="col-lg-8 col-xl-6 mb-3 d-flex justify-center align-items-center"
          style="color: #585858; background: #d4d4d4; border-radius: 5px"
        >
          {{
            $t(
              "The investor network diagram is only visible for live versions of an investor. I.e. https://landmatrix.org/investor/:id/"
            )
          }}
        </div>
      </div>

      <div v-if="investor.datasources && investor.datasources.length > 0">
        <h3>{{ $t("Data sources") }} ({{ investor.datasources.length }})</h3>
        <table class="bigtable">
          <thead>
            <tr>
              <th v-for="field in deal_submodel_sections.datasource" :key="field">
                <FieldLabel :fieldname="field" model="datasource" />
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ds in investor.datasources" :key="ds.id">
              <td v-for="field in deal_submodel_sections.datasource" :key="field">
                <DisplayField
                  :show-label="false"
                  :value="ds[field]"
                  :value-classes="[]"
                  :wrapper-classes="['text-center']"
                  :fieldname="field"
                  model="datasource"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <h3>{{ $t("Involvements") }} ({{ simple_involvements.length }})</h3>
      <table class="bigtable">
        <thead>
          <tr>
            <th>{{ $t("Investor ID") }}</th>
            <th>{{ $t("Name") }}</th>
            <th>{{ $t("Country of registration") }}</th>
            <th>{{ $t("Classification") }}</th>
            <th>{{ $t("Relationship") }}</th>
            <th>{{ $t("Ownership share") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="involvement in simple_involvements" :key="involvement.id">
            <td>
              <DisplayField
                :show-label="false"
                :value="involvement.investor.id"
                :value-classes="[]"
                :wrapper-classes="['text-center']"
                fieldname="id"
                model="investor"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="involvement.investor.name"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="name"
                model="investor"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="involvement.investor.country"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="country"
                model="investor"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="involvement.investor.classification"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="classification"
                model="investor"
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

      <h3 v-if="investor.deals">
        {{ $t("Deals (Involvements as Operating company)") }} ({{
          investor.deals.length
        }})
      </h3>

      <table v-if="investor.deals" class="bigtable">
        <thead>
          <tr>
            <th>{{ $t("Deal ID") }}</th>
            <th>{{ $t("Target country") }}</th>
            <th>{{ $t("Intention of investment") }}</th>
            <th>{{ $t("Current negotiation status") }}</th>
            <th>{{ $t("Current implementation status") }}</th>
            <th>{{ $t("Deal size") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="deal in investor.deals" :key="deal.id">
            <td>
              <DisplayField
                :show-label="false"
                :value="deal.id"
                :value-classes="[]"
                :wrapper-classes="['text-center']"
                fieldname="id"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="deal.country"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="country"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="deal.current_intention_of_investment"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="current_intention_of_investment"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="deal.current_negotiation_status"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="current_negotiation_status"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="deal.current_implementation_status"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="current_implementation_status"
              />
            </td>
            <td>
              <DisplayField
                :show-label="false"
                :value="deal.deal_size"
                :value-classes="[]"
                :wrapper-classes="[]"
                fieldname="deal_size"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <!--      <b-tabs v-if="graphDataIsReady" content-class="mb-3">-->

      <!--        <b-tab v-if="'deals' in investor">-->
      <!--          <template #title>-->
      <!--            <h5>-->
      <!--              -->
      <!--              ({{ investor.deals.length }})-->
      <!--            </h5>-->
      <!--          </template>-->
      <!--          <table class="table data-table">-->

      <!--            <tbody>-->
      <!--              <tr v-for="deal in deals" :key="deal.id">-->
      <!--                -->
      <!--              </tr>-->
      <!--            </tbody>-->
      <!--          </table>-->
      <!--        </b-tab>-->
      <!--        <b-tab>-->
      <!--          <template #title>-->
      <!--            <h5>{{ $t("Investor history") }}</h5>-->
      <!--          </template>-->
      <!--          <InvestorHistory-->
      <!--            :investor="investor"-->
      <!--            :investor-id="investorId"-->
      <!--            :investor-version="investorVersion"-->
      <!--          />-->
      <!--        </b-tab>-->
      <!--      </b-tabs>-->
    </div>
  </div>
  <div v-else class="row" style="height: 100%">
    <LoadingPulse />
  </div>
</template>

<script lang="ts">
  import LoadingPulse from "$components/Data/LoadingPulse";
  import DisplayField from "$components/Fields/DisplayField";
  import FieldLabel from "$components/Fields/FieldLabel.vue";
  import HeaderDates from "$components/HeaderDates";
  import InvestorGraph from "$components/Investor/InvestorGraph";
  import InvestorManageHeader from "$components/Investor/InvestorManageHeader";
  import store from "$store";
  import { investor_gql_query } from "$store/queries";
  import { deal_submodel_sections } from "$views/Deal/deal_sections";
  import gql from "graphql-tag";
  import Vue from "vue";

  export default Vue.extend({
    name: "InvestorDetail",
    components: {
      FieldLabel,
      DisplayField,
      HeaderDates,
      InvestorGraph,
      InvestorManageHeader,
      LoadingPulse,
    },
    props: {
      investorId: { type: [Number, String], required: true },
      investorVersion: { type: [Number, String], default: null },
    },
    metaInfo() {
      return { title: this.title };
    },
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
        title: "Investor",
        deal_submodel_sections,
      };
    },
    apollo: {
      investor: {
        query: investor_gql_query,
        variables() {
          return {
            id: +this.investorId,
            version: +this.investorVersion,
            subset: this.$store.getters.userAuthenticated ? "UNFILTERED" : "PUBLIC",
            depth: this.depth,
            includeDeals: this.includeDealsInQuery,
          };
        },
        update({ investor }) {
          if (!investor) this.$router.push({ name: "list_investors" });
          if (investor.status === 1 && !this.investorVersion)
            this.$router.push({
              name: "investor_detail",
              params: {
                investorId: this.investorId,
                investorVersion: investor.versions[0]?.id,
              },
            });

          return investor;
        },
        fetchPolicy: "no-cache",
      },
    },
    computed: {
      simple_involvements() {
        return [
          ...this.investor.investors.map((i) => ({
            ...i,
            involvement_type: "INVESTOR",
          })),
          ...this.investor.ventures.map((i) => ({
            ...i,
            investor: i.venture,
            involvement_type: "VENTURE",
          })),
        ];
      },
      userAuthenticated() {
        return this.$store.state.user?.is_authenticated;
      },
      involvements() {
        return this.investor.involvements || [];
      },

      graphDataIsReady() {
        return (
          this.investor &&
          "involvements" in this.investor &&
          "deals" in this.investor &&
          !this.$apollo.queries.investor.loading
        );
      },
    },
    watch: {
      investorId(investorId, oldInvestorId) {
        if (investorId !== oldInvestorId) {
          this.includeDealsInQuery = false;
        }
      },
      investor(investor, oldInvestor) {
        if (!oldInvestor) {
          // initial load complete, also load deals
          this.includeDealsInQuery = true;
          this.depth = 1;
        }
        this.title = `${investor.name} (#${investor.id})`;
        store.dispatch("setPageContext", {
          breadcrumbs: [
            { link: { name: "wagtail" }, name: "Home" },
            { link: { name: "list_investors" }, name: "Data" },
            { name: this.title },
          ],
        });
      },
    },
    methods: {
      changeStatus({ transition, comment = "", to_user = null }) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation (
                $id: Int!
                $version: Int!
                $transition: WorkflowTransition!
                $comment: String
                $to_user_id: Int
              ) {
                change_investor_status(
                  id: $id
                  version: $version
                  transition: $transition
                  comment: $comment
                  to_user_id: $to_user_id
                ) {
                  investorId
                  investorVersion
                }
              }
            `,
            variables: {
              id: +this.investorId,
              version: this.investorVersion ? +this.investorVersion : null,
              transition,
              comment,
              to_user_id: to_user ? to_user.id : null,
            },
          })
          .then(({ data: { change_investor_status } }) => {
            if (transition === "ACTIVATE") {
              this.$router.push({
                name: "investor_detail",
                params: { investorId: change_investor_status.investorId.toString() },
              });
            } else {
              if (
                parseInt(this.investorVersion) !==
                change_investor_status.investorVersion
              ) {
                this.$router.push({
                  name: "investor_detail",
                  params: {
                    investorId: change_investor_status.investorId.toString(),
                    investorVersion: change_investor_status.investorVersion.toString(),
                  },
                });
              } else {
                console.log("Investor detail: reload");
                this.reloadInvestor();
              }
            }
          })
          .catch((error) => console.error(error));
      },
      deleteInvestor(comment) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation ($id: Int!, $version: Int, $comment: String) {
                investor_delete(id: $id, version: $version, comment: $comment)
              }
            `,
            variables: {
              id: +this.investorId,
              version: this.investorVersion ? +this.investorVersion : null,
              comment,
            },
          })
          .then(() => {
            if (this.investorVersion) {
              this.$router
                .push({
                  name: "investor_detail",
                  params: { investorId: this.investorId.toString() },
                })
                .then(this.reloadInvestor);
            }
            this.reloadInvestor();
          });
      },
      copyInvestor(): void {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation ($id: Int!) {
                object_copy(otype: "investor", obj_id: $id) {
                  objId
                  objVersion
                }
              }
            `,
            variables: { id: +this.investorId },
          })
          .then(({ data }) => {
            window.open(
              this.$router.resolve({
                name: "investor_detail",
                params: {
                  investorId: data.object_copy.objId,
                  investorVersion: data.object_copy.objVersion,
                },
              }).href,
              "_blank"
            );
          });
      },
      reloadInvestor() {
        console.log("Investor detail: reload");
        this.$apollo.queries.investor.refetch();
      },
      detect_role(/** @type {Involvement} */ involvement) {
        if (involvement.role === "PARENT") {
          if (involvement.involvement_type === "INVESTOR")
            return this.$t("Parent company");
          if (involvement.involvement_type === "VENTURE")
            return this.$t("Subsidiary company");
        }
        if (involvement.role === "LENDER") {
          if (involvement.involvement_type === "INVESTOR")
            return this.$t("Tertiary investor/lender");
          if (involvement.involvement_type === "VENTURE")
            return this.$t("Beneficiary company");
        }
      },
      onNewDepth(value) {
        if (value > this.depth) {
          this.depth = +value;
        }
      },
    },
  });
</script>

<style lang="scss" scoped>
  .investor-detail {
    h1 {
      color: var(--color-lm-dark);
      text-align: left;
      text-transform: none;

      &:before {
        display: none;
      }
    }
  }
</style>
