<template>
  <div class="container" v-if="investor">
    <b-tabs content-class="mt-3">
      <b-tab title="General Info">
        <div>
          <h3>Name</h3>
          <p>{{ investor.name }}</p>
          <h3>Country of registration/origin</h3>
          <p>{{ investor.country.name }}</p>
          <h3>Classification</h3>
          <p>{{ investor.classification }}</p>
          <h3>Comment</h3>
          <p>{{ investor.comment }}</p>
        </div>
      </b-tab>
      <b-tab :title="`Parent companies (${parents.length})`">
        <div v-for="(involvement, i) in parents">
          <h3>
            Parent company <small>#{{(i+1)}}</small>
          </h3>
          <div class="row">
            <div class="col-md-3">Investor</div>
            <div class="col-md-9">
              <a :href="`/investor/${involvement.investor.id}/`">
                {{ involvement.investor.name }} (#{{ involvement.investor.id }})
              </a>
            </div>
          </div>
          <div class="row" v-if="involvement.percentage">
            <div class="col-md-3">Ownership share</div>
            <div class="col-md-9">
                {{ involvement.percentage }}
            </div>
          </div>
        </div>
        {{  }}
      </b-tab>
      <b-tab title="Tertiary investors/lenders"></b-tab>
      <b-tab :title="`Involvements as Parent Company (${parent_of.length})`">
        <div v-for="(involvement, i) in parent_of">
          <h3>
            Involvement <small>#{{(i+1)}}</small>
          </h3>
          <div class="row">
            <div class="col-md-3">Investor</div>
            <div class="col-md-9">
              <a :href="`/investor/${involvement.venture.id}/`">
                {{ involvement.venture.name }} (#{{ involvement.venture.id }})
              </a>
            </div>
          </div>
          <div class="row" v-if="involvement.percentage">
            <div class="col-md-3">Ownership share</div>
            <div class="col-md-9">
                {{ involvement.percentage }}
            </div>
          </div>
        </div>
      </b-tab>

      <b-tab title="Involvements as Tertiary investor/lender"></b-tab>
      <b-tab :title="`Deals (Involvements as Operating company) (${investor.deals.length})`">
        <div v-for="deal in investor.deals">
          <router-link :to="{ name: 'deal_detail', params: { deal_id: deal.id } }">
            {{ deal.id }}
          </router-link>
        </div>
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
      parent_of() {
        return this.involvements.filter((x) => {
          return x.role === "STAKEHOLDER" && x.investor.id === this.investor.id;
        });
      },
      parents() {
        return this.involvements.filter((x) => {
          return x.role === "STAKEHOLDER" && x.venture.id === this.investor.id;
        });
      },
    },
    methods: {
      general_info(investor) {
        return {
          Name: investor.name,
          "Country of registration/origin": investor.country.name,
          Classification: investor.classification,
          Comment: investor.comment,
        };
      },
    },
    beforeRouteEnter(to, from, next) {
      store.dispatch("setCurrentInvestor", to.params.investor_id);
      next();
    },
    beforeRouteLeave(to, from, next) {
      store.dispatch("setCurrentDeal", {});
      next();
    },
  };
</script>
