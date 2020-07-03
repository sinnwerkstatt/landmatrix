<template>
  <div class="container" v-if="investor">
    <h2>General Info</h2>
    <dl class="row">
      <dt class="col-3">Name</dt>
      <dd class="col-9">{{ investor.name }}</dd>
    </dl>
    <dl class="row">
      <dt class="col-3">Country of registration/origin</dt>
      <dd class="col-9">{{ investor.country.name }}</dd>
    </dl>
    <dl class="row">
      <dt class="col-3">Classification</dt>
      <dd class="col-9">{{ investor.classification }}</dd>
    </dl>
    <dl class="row">
      <dt class="col-3">Comment</dt>
      <dd class="col-9">{{ investor.comment }}</dd>
    </dl>

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
                >
                  #{{ involvement.investor.id }}
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
                >
                  #{{ deal.id }}
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
</template>

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }
</style>
<script>
  import store from "@/store";

  export default {
    props: ["investor_id"],
    data() {
      return {};
    },
    computed: {
      investor() {
        return this.$store.state.investor.current_investor;
      },
      involvements() {
        return this.investor.involvements;
      },
    },
    methods: {
      detect_role(investor) {
        console.log(investor.id, investor.role, investor.involvement_type);
        if (investor.role === "STAKEHOLDER") {
          if (investor.involvement_type === "INVESTOR") return "Parent company";
          if (investor.involvement_type === "VENTURE")  return "Involved in as Parent Company";
        }
        if (investor.role === "INVESTOR") {
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
