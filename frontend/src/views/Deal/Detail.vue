<template>
  <div class="container" v-if="deal && deal_fields">
    <div class="loadingscreen" v-if="loading">
      <div class="loader"></div>
    </div>
<!--    <div class="quicknav">-->
<!--      <div v-for="(version, i) in deal.versions">-->
<!--        <span v-if="(!deal_version && !i) || +deal_version === +version.revision.id"-->
<!--          >Current</span-->
<!--        >-->
<!--        <router-link-->
<!--          v-else-->
<!--          :to="{-->
<!--            name: 'deal_detail',-->
<!--            params: { deal_id, deal_version: version.revision.id },-->
<!--          }"-->
<!--          >{{ version.revision.date_created | defaultdate }}</router-link-->
<!--        >-->
<!--      </div>-->
<!--    </div>-->
    <b-tabs
      content-class="mt-3"
      vertical
      pills
      nav-wrapper-class="position-relative"
      nav-class="sticky-nav"
      :key="deal_id + deal_version"
    >
      <DealLocationSection
        :title="deal_fields.location.label"
        :deal="deal"
        :fields="deal_fields.location.fields"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.general_info.label"
        :deal="deal"
        :sections="deal_fields.general_info.subsections"
        :readonly="true"
      />

      <DealSubmodelSection
        :title="deal_fields.contract.label"
        :submodel="deal.contracts"
        :fields="deal_fields.contract.fields"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.employment.label"
        :deal="deal"
        :sections="deal_fields.employment.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.investor_info.label"
        :deal="deal"
        :sections="deal_fields.investor_info.subsections"
        :readonly="true"
      />

      <DealSubmodelSection
        :title="deal_fields.datasource.label"
        :submodel="deal.datasources"
        :fields="deal_fields.datasource.fields"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.local_communities.label"
        :deal="deal"
        :sections="deal_fields.local_communities.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.former_use.label"
        :deal="deal"
        :sections="deal_fields.former_use.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.produce_info.label"
        :deal="deal"
        :sections="deal_fields.produce_info.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.water.label"
        :deal="deal"
        :sections="deal_fields.water.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.gender_related_info.label"
        :deal="deal"
        :sections="deal_fields.gender_related_info.subsections"
        :readonly="true"
      />

      <DealSection
        :title="deal_fields.guidelines_and_principles.label"
        :deal="deal"
        :sections="deal_fields.guidelines_and_principles.subsections"
        :readonly="true"
      />

      <b-tab disabled>
        <template v-slot:title>
          <hr />
        </template>
      </b-tab>

      <b-tab title="Deal History">
        <div>
          <h3>History</h3>
          <table class="table table-condensed">
            <thead>
              <tr>
                <th class="">Timestamp</th>
                <th class="">User</th>
                <th class="">Fully updated</th>
                <th class="">Status</th>
                <th class="">Comment</th>
                <th class=""><i class="fa fa-eye" aria-hidden="true"></i></th>
                <th class=""></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(version, i) in deal.versions">
                <td>{{ version.revision.date_created | defaultdate }}</td>
                <td>{{ version.revision.user && version.revision.user.full_name }}</td>
                <td>{{ version.deal.fully_updated ? "✓" : "" }}</td>
                <td>
                  {{ derive_status(version.deal.status, version.deal.draft_status) }}
                </td>
                <td>{{ version.revision.comment }}</td>
                <td>
                  <span
                    v-if="
                      (!deal_version && !i) || +deal_version === +version.revision.id
                    "
                    >Current</span
                  >
                  <router-link
                    v-else
                    :to="{
                      name: 'deal_detail',
                      params: { deal_id, deal_version: version.revision.id },
                    }"
                    v-slot="{ href, navigate }"
                  >
                    <!-- this hack helps to understand that a new version is actually loading, atm -->
                    <a :href="href" @click="navigate">Show</a>
                  </router-link>
                </td>
                <td>
                  <span :href="`/newdeal/deal/compare/${version.revision.id}/`">
                    Compare with previous<br>not working yet
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import store from "/store";
  import DealSection from "/components/Deal/DealSection";
  import DealLocationSection from "/components/Deal/DealLocationsSection";
  import DealSubmodelSection from "/components/Deal/DealSubmodelSection";
  import { derive_status } from "/utils";
  import { mapState } from "vuex";

  export default {
    props: ["deal_id", "deal_version"],
    components: {
      DealSection,
      DealLocationSection,
      DealSubmodelSection,
    },
    data() {
      return {
        loading: false,
      };
    },
    methods: {
      derive_status,
    },
    computed: {
      ...mapState({
        deal_fields: (state) => state.deal.deal_fields,
      }),
      deal() {
        return this.$store.state.deal.current_deal;
      },
    },
    beforeRouteEnter(to, from, next) {
      store
        .dispatch("setCurrentDeal", {
          deal_id: to.params.deal_id,
          deal_version: to.params.deal_version,
        })
        .then(() => next())
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
    beforeRouteUpdate(to, from, next) {
      this.loading = true;
      store
        .dispatch("setCurrentDeal", {
          deal_id: to.params.deal_id,
          deal_version: to.params.deal_version,
        })
        .then(() => {
          this.loading = false;
          next();
        })
        .catch(() => next({ name: "404", params: [to.path], replace: true }));
    },
  };
</script>

<style lang="scss">
  .sticky-nav {
    position: -webkit-sticky;
    position: sticky;
    top: 10%;
    z-index: 99;
  }

  div.quicknav {
    z-index: 100;
    position: absolute;
    right: 200px;
    width: 200px;
    height: 100%;
    background: rgba(255, 255, 255, 0.7);
  }
</style>
