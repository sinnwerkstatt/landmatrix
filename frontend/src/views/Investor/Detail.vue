<template>
  <div v-if="investor">
    <InvestorManageHeader
      v-if="manage"
      :object="investor"
      :object-version="investorVersion"
      @change_status="change_investor_status"
      @reload="reload_investor"
      @delete="delete_investor"
    />
    <div v-else class="container investor-detail">
      <div class="row">
        <div>
          <h1>
            {{ investor.name }} <small>#{{ investor.id }}</small>
          </h1>
        </div>
        <div class="panel-container ml-auto">
          <a
            v-if="$store.getters.userAuthenticated"
            :href="`/legacy/investor/edit/${investor.id}/`"
            target="_blank"
          >
            <i class="fas fa-edit" /> {{ $t("Edit") }}
          </a>
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
          class="col-lg-8 col-xl-6 mb-3"
          :class="{ loading_wrapper: !graphDataIsReady }"
        >
          <div v-if="!graphDataIsReady" style="height: 400px">
            <LoadingPulse />
          </div>
          <InvestorGraph
            v-else
            :investor="investor"
            :init-depth="depth"
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
              "You're viewing an old version of this Investor, for which we don't have this diagram. To avoid confusion, it is deactivated here."
            )
          }}
        </div>
      </div>

      <b-tabs v-if="graphDataIsReady" content-class="mb-3">
        <b-tab>
          <template #title>
            <h5>{{ $t("Involvements") }} ({{ involvements.length }})</h5>
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
              <tr v-for="involvement in involvements" :key="involvement.id">
                <td>
                  <DisplayField
                    :wrapper-classes="['text-center']"
                    :value-classes="[]"
                    fieldname="id"
                    :value="involvement.investor.id"
                    model="investor"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="name"
                    :value="involvement.investor.name"
                    model="investor"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="country"
                    :value="involvement.investor.country"
                    model="investor"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="classification"
                    :value="involvement.investor.classification"
                    model="investor"
                    :show-label="false"
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
          <template #title>
            <h5>
              {{ $t("Deals (Involvements as Operating company)") }}
              ({{ investor.deals.length }})
            </h5>
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
              <tr v-for="deal in deals" :key="deal.id">
                <td>
                  <DisplayField
                    :wrapper-classes="['text-center']"
                    :value-classes="[]"
                    fieldname="id"
                    :value="deal.id"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="country"
                    :value="deal.country"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="current_intention_of_investment"
                    :value="deal.current_intention_of_investment"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="current_negotiation_status"
                    :value="deal.current_negotiation_status"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="current_implementation_status"
                    :value="deal.current_implementation_status"
                    :show-label="false"
                  />
                </td>
                <td>
                  <DisplayField
                    :wrapper-classes="[]"
                    :value-classes="[]"
                    fieldname="deal_size"
                    :value="deal.deal_size"
                    :show-label="false"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </b-tab>
        <b-tab>
          <template #title>
            <h5>{{ $t("Investor history") }}</h5>
          </template>
          <InvestorHistory
            :investor="investor"
            :investor-id="investorId"
            :investor-version="investorVersion"
          />
        </b-tab>
      </b-tabs>
    </div>
  </div>
  <div v-else class="row" style="height: 100%">
    <LoadingPulse />
  </div>
</template>

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";
  import DisplayField from "$components/Fields/DisplayField";
  import HeaderDates from "$components/HeaderDates";
  import InvestorGraph from "$components/Investor/InvestorGraph";
  import InvestorHistory from "$components/Investor/InvestorHistory";
  import InvestorManageHeader from "$components/Investor/InvestorManageHeader";
  import store from "$store";
  import { investor_query } from "$store/queries";
  import gql from "graphql-tag";
  import { mapState } from "vuex";

  export default {
    name: "InvestorDetail",
    components: {
      InvestorManageHeader,
      HeaderDates,
      InvestorHistory,
      LoadingPulse,
      InvestorGraph,
      DisplayField,
    },
    props: {
      investorId: { type: [Number, String], required: true },
      investorVersion: { type: [Number, String], default: null },
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
      };
    },
    metaInfo() {
      return { title: this.title };
    },
    apollo: { investor: investor_query },
    computed: {
      manage() {
        return (
          this.$store.state.page.user && this.$store.state.page.user.is_authenticated
        );
      },
      ...mapState({
        formFields: (state) => state.formfields,
      }),
      involvements() {
        return this.investor.involvements || [];
      },
      deals() {
        return this.investor?.deals ?? [];
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
      change_investor_status({ transition, comment = null, to_user = null }) {
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
                this.reload_investor();
              }
            }
          })
          .catch((error) => console.error(error));
      },
      delete_investor(comment) {
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
                .then(this.reload_investor);
            }
            this.reload_investor();
          });
      },
      reload_investor() {
        console.log("Investor detail: reload");
        this.$apollo.queries.investor.refetch();
      },
      detect_role(/** @type {Involvement} */ involvement) {
        if (involvement.role === "PARENT") {
          if (involvement.involvement_type === "INVESTOR") return "Parent company";
          if (involvement.involvement_type === "VENTURE")
            return "Involved in as Parent Company";
        }
        if (involvement.role === "LENDER") {
          if (involvement.involvement_type === "INVESTOR")
            return "Tertiary investor/lender";
          if (involvement.involvement_type === "VENTURE")
            return "Involved in as Tertiary investor/lender";
        }
      },
      onNewDepth(value) {
        if (value > this.depth) {
          this.depth = +value;
        }
      },
    },
  };
</script>

<style lang="scss">
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
