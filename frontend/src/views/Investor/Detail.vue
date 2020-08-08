<template>
  <div>
    <div class="loadingscreen" v-if="!investor">
      <div class="loader"></div>
    </div>

    <div class="container" v-if="investor">
      <h2>General Info</h2>
      <div class="row">
        <div class="col">
          <dl class="row">
            <template v-for="(name, field) in fields" v-if="investor[field]">
              <dt class="col-3">{{ name }}</dt>
              <dd class="col-9">{{ investor[field] }}</dd>
            </template>
          </dl>
        </div>
        <div class="col">
          <InvestorGraph
            v-if="involvements.length"
            :investor="investor"
          ></InvestorGraph>
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
  import InvestorGraph from "/components/Investor/InvestorGraph";

  export default {
    name: "InvestorDetail",
    components: { InvestorGraph },
    props: ["investor_id"],
    data() {
      return {
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
      investor() {
        let investor = this.$store.state.investor.current_investor;
        if (investor) return { ...investor, country: investor.country.name };
      },
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
    beforeRouteEnter(to, from, next) {
      store.dispatch("setCurrentInvestor", to.params.investor_id);
      next();
    },
    beforeRouteUpdate(to, from, next) {
      store.dispatch("setCurrentInvestor", to.params.investor_id);
      next();
    },
  };
</script>
